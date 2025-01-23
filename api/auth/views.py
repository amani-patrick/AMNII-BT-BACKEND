from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny


# Signup View
@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response('User created successfully.', RegisterSerializer),
        400: 'Bad Request - Validation errors',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """User Signup (Registration)."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User created successfully.',
            'user': RegisterSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            'Login successful.',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                },
            )
        ),
        400: 'Invalid credentials or validation errors'
    }
)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User Login with JWT authentication."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout View
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='The refresh token to blacklist'),
        },
        required=['refresh_token'],
    ),
    responses={
        200: 'Successfully logged out',
        400: 'Bad Request - Missing or invalid refresh token',
    }
)
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
