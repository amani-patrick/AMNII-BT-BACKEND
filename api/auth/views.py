from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer

# Signup View
@api_view(['POST'])
def signup(request):
    """User Signup (Registration)."""
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully.',
                'user': RegisterSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
@api_view(['POST'])
def login(request):
    """User Login with JWT authentication."""
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Authenticate the user with provided credentials
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                # Create JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                })
            return Response({"message": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout View
@api_view(['POST'])
def logout(request):
    """User Logout (Invalidate the refresh token)."""
    try:
        # Get the refresh token from the request's body
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a RefreshToken instance from the provided token
        token = RefreshToken(refresh_token)
        
        # Revoke the token (Blacklist it)
        token.blacklist()
        
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"message": f"Error logging out: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
