import subprocess
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.accounts.models import TradingAccount

# Dictionary to store the running bot processes
bot_processes = {}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_bot(request):
    """Start the trading bot with account credentials."""
    token = request.headers.get('Authorization', None)
    if not token or not token.startswith('Bearer '):
        return Response({"message": "Authentication token is required."}, status=401)
    
    account_name = request.data.get("account_name")
    login = request.data.get("login")
    server = request.data.get("server")
    
    # Password is no longer required from the frontend
    if not account_name or not login or not server:
        return Response({"message": "All parameters (account_name, login, server) are required."}, status=400)
    
    try:
        # Fetch the trading account from the database
        trading_account = TradingAccount.objects.get(user=request.user, name=account_name)
        account_number = trading_account.account_number
        broker_server = trading_account.broker_server
        password = trading_account.passwd  # Retrieve password from the database
    except TradingAccount.DoesNotExist:
        return Response({"message": f"Trading account '{account_name}' not found."}, status=404)
    
    # Check if the bot is already running for the account
    if account_number in bot_processes and bot_processes[account_number].poll() is None:
        return Response({"message": f"Bot for account {account_number} is already running!"}, status=400)

    # Define paths for the virtual environment and main script
    venv_python_path = r"C:\Users\amnii\Documents\2025\Trade\venv\Scripts\python.exe" 
    main_script_path = r"C:\Users\amnii\Documents\2025\Trade\main.py" 

    # Command to start the bot
    command = [
        venv_python_path,
        main_script_path,
        "--login", login,
        "--server", server,
        "--password", password,  # Use the password retrieved from the database
        "--token", token
    ]

    try:
        # Start the bot process
        bot_process = subprocess.Popen(
            command, 
            shell=True,  
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Store the process in the bot_processes dictionary
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_bot_status(request):
    """Fetch the current status of the bot."""
    account_name = request.data.get("account_name")
    if not account_name:
        return Response({"message": "Account name is required."}, status=400)
    try:
        trading_account = TradingAccount.objects.get(user=request.user, name=account_name)
        account_number = trading_account.account_number
    except TradingAccount.DoesNotExist:
        return Response({"message": f"Trading account '{account_name}' not found."}, status=404)

    if account_number in bot_processes and bot_processes[account_number].poll() is None:
        return Response({"status": "running"})
    else:
        return Response({"status": "stopped"})