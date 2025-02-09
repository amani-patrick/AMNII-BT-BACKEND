import subprocess
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.accounts.models import TradingAccount
from rest_framework.authentication import TokenAuthentication

bot_processes = {}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_bot(request):
    """Start the trading bot with account credentials."""
    # Extract the token from the request header for authentication
    token = request.headers.get('Authorization', None)
    
    if not token or not token.startswith('Bearer '):
        return Response({"message": "Authentication token is required."}, status=401)

    account_name = request.data.get("account_name")
    login = request.data.get("login")
    server = request.data.get("server")
    password = request.data.get("password")
    
    if not account_name or not login or not server or not password:
        return Response({"message": "All parameters (account_name, login, server, password) are required."}, status=400)

    try:
        trading_account = TradingAccount.objects.get(user=request.user, name=account_name)
    except TradingAccount.DoesNotExist:
        return Response({"message": f"Trading account '{account_name}' not found."}, status=404)
    
    account_number = trading_account.account_number
    broker_server = trading_account.broker_server  # Use the server value passed from the frontend

    # Check if the bot is already running for the account
    if account_number in bot_processes and bot_processes[account_number].poll() is None:
        return Response({"message": f"Bot for account {account_number} is already running!"}, status=400)

    # Build the command with arguments to pass to the script
    try:
        bot_process = subprocess.Popen(
            ["python", "C:\\Users\\amnii\\Documents\\2025\\Trade\\main.py", 
             "--login", login, 
             "--server", server, 
             "--password", password, 
             "--token", token],  # Pass the authentication token as an argument
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        bot_processes[account_number] = bot_process

        return Response({"message": f"Bot for account {account_number} started successfully!"})
    except Exception as e:
        return Response({"message": f"Failed to start bot for account {account_number}: {str(e)}"}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_bot(request):
    """Stop the trading bot."""
    account_name = request.data.get("account_name")
    
    if not account_name:
        return Response({"message": "Account name is required."}, status=400)

    try:
        trading_account = TradingAccount.objects.get(user=request.user, name=account_name)
        account_number = trading_account.account_number
    except TradingAccount.DoesNotExist:
        return Response({"message": f"Trading account '{account_name}' not found."}, status=404)

    if account_number not in bot_processes or bot_processes[account_number].poll() is not None:
        return Response({"message": f"Bot for account {account_number} is not running!"}, status=400)

    try:
        bot_processes[account_number].terminate()
        bot_processes[account_number].wait()
        del bot_processes[account_number]  
        return Response({"message": f"Bot for account {account_number} stopped successfully!"})
    except Exception as e:
        return Response({"message": f"Failed to stop bot for account {account_number}: {str(e)}"}, status=500)
@api_view(['POST'])  # Change to POST since we are now expecting data in the body
@permission_classes([IsAuthenticated])
def get_bot_status(request):
    """Fetch the current status of the bot."""
    
    # Get the account_name from the body of the request
    account_name = request.data.get("account_name")
    
    if not account_name:
        return Response({"message": "Account name is required."}, status=400)

    try:
        # Retrieve the TradingAccount for the authenticated user and the specified account name
        trading_account = TradingAccount.objects.get(user=request.user, name=account_name)
        account_number = trading_account.account_number
    except TradingAccount.DoesNotExist:
        return Response({"message": f"Trading account '{account_name}' not found."}, status=404)

    if account_number in bot_processes and bot_processes[account_number].poll() is None:
        return Response({"status": "running"})
    else:
        return Response({"status": "stopped"})
