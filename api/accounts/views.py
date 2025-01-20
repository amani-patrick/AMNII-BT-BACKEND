from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import TradingAccount
from .serializers import TradingAccountSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    """Fetch all trading accounts for the authenticated user."""
    accounts = TradingAccount.objects.filter(user=request.user)
    serializer = TradingAccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_account(request):
    """Add a new trading account."""
    data = request.data
    data['user'] = request.user.id
    serializer = TradingAccountSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_account(request, account_id):
    """Update an existing trading account."""
    try:
        account = TradingAccount.objects.get(id=account_id, user=request.user)
    except TradingAccount.DoesNotExist:
        return Response({"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TradingAccountSerializer(account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request, account_id):
    """Delete a trading account."""
    try:
        account = TradingAccount.objects.get(id=account_id, user=request.user)
        account.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except TradingAccount.DoesNotExist:
        return Response({"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
