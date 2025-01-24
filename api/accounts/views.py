from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import TradingAccount
from django.contrib.auth.hashers import make_password
from .serializers import TradingAccountSerializer

# View for fetching all trading accounts for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    """Fetch all trading accounts for the authenticated user."""
    accounts = TradingAccount.objects.filter(user=request.user)
    serializer = TradingAccountSerializer(accounts, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated before creating an account
def add_account(request):
    if request.method == 'POST':
        # Ensure the authenticated user is assigned to the TradingAccount
        serializer = TradingAccountSerializer(data=request.data)
        
        # Check if the serializer is valid
        if serializer.is_valid():
            # Attach the authenticated user
            serializer.validated_data['user'] = request.user
            
            # Handle password securely before saving the account
            password = serializer.validated_data.pop('password', None)  # Remove password from validated data
            account = serializer.save()  # Save the account first

            # Set password securely using make_password
            if password:
                account.password = make_password(password)  # Hash the password
                account.save()  # Save account again after setting the password

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for updating an existing trading account
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_account(request, account_name):
    """Update an existing trading account by its name."""
    try:
        # Find the account by name and ensure it belongs to the authenticated user
        account = TradingAccount.objects.get(name=account_name, user=request.user)
    except TradingAccount.DoesNotExist:
        return Response({"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

    # Serialize and update the account
    serializer = TradingAccountSerializer(account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request, account_name):
    """Delete a trading account by its name."""
    try:
        # Find the account by name and ensure it belongs to the authenticated user
        account = TradingAccount.objects.get(name=account_name, user=request.user)
        account.delete()  # Delete the account if found
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except TradingAccount.DoesNotExist:
        return Response({"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND)