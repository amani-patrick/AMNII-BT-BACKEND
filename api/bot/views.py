import subprocess
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Global variable to store the subprocess
bot_process = None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_bot(request):
    """Start the trading bot."""
    global bot_process

    if bot_process is not None and bot_process.poll() is None:
        return Response({"message": "Bot is already running!"}, status=400)

    try:

        bot_process = subprocess.Popen(
            ["python", "Trade.py"],  # Adjust the path to Trade.py if needed
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return Response({"message": "Bot started successfully!"})
    except Exception as e:
        return Response({"message": f"Failed to start bot: {str(e)}"}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_bot(request):
    """Stop the trading bot."""
    global bot_process

    if bot_process is None or bot_process.poll() is not None:
        return Response({"message": "Bot is not running!"}, status=400)

    try:
        bot_process.terminate()
        bot_process.wait() 
        bot_process = None
        return Response({"message": "Bot stopped successfully!"})
    except Exception as e:
        return Response({"message": f"Failed to stop bot: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bot_status(request):
    """Fetch the current status of the bot."""
    global bot_process

    if bot_process is not None and bot_process.poll() is None:
        return Response({"status": "running"})
    else:
        return Response({"status": "stopped"})
