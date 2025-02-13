from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import exception_handler
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.exceptions import TokenError


# User registration endpoint
@api_view(['POST'])
def signup(request):
    """
    User registration endpoint.
    Creates a new user, sets a password, and returns an access token.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Create the user using the serializer

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Build response data
        response_data = {
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'access_token': access_token,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate a user, return an access token, and set a refresh token in the response.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Response with access and refresh tokens
        response = Response(
            {
                'access_token': access_token,
                'refresh_token': refresh_token,  # Include the refresh token in the response
            },
            status=status.HTTP_200_OK,
        )

        # Optionally, you can also set the refresh token as an HTTP-only cookie
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,  # Use True in production
            samesite='Strict',  # Adjust based on your app's requirements
        )

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User logout endpoint (Invalidate the refresh token)
@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """User Logout (Invalidate the refresh token)."""
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": f"Error logging out: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# Custom exception handler
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        # Customize the message
        response.data = {'message': 'Unauthorised! Access denied '}
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Custom token refresh endpoint.
    Accepts a valid refresh token and returns a new access token.
    """
    refresh_token = request.data.get('refresh')  # Get the refresh token from the request body
    
    if not refresh_token:
        return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        # Check if the token is blacklisted
        token.check_blacklist()  # This will raise an error if the token is blacklisted
        
        # Generate new tokens
        new_refresh_token = str(token)
        new_access_token = str(token.access_token)
        
        return Response({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }, status=status.HTTP_200_OK)

    except TokenError:
        return Response({"message": "The refresh token is blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": f"Error refreshing token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
