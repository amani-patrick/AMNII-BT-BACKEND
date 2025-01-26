from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from .models import Strategy


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_strategies(request):
    """
    Fetch all strategies for the authenticated user.
    Only returns strategies owned by the current user.
    """
    strategies = Strategy.objects.filter(user=request.user).values(
        'id', 'name', 'description', 'parameters'
    )
    return Response(list(strategies), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser]) 
def create_strategy(request):
    """
    Create a new trading strategy. Only admin users are allowed to create strategies.
    """
    name = request.data.get('name')
    description = request.data.get('description')
    parameters = request.data.get('parameters', {})

    if not name or not description:
        return Response({"detail": "Name and description are required."}, status=status.HTTP_400_BAD_REQUEST)

    Strategy.objects.create(
        user=request.user,
        name=name,
        description=description,
        parameters=parameters,
    )
    return Response({"message": "Strategy created successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_strategy(request, strategy_id):
    """
    Update an existing trading strategy. Only the owner of the strategy can update it.
    """
    try:
        strategy = Strategy.objects.get(id=strategy_id, user=request.user)
    except Strategy.DoesNotExist:
        return Response({"detail": "Strategy not found or you do not have permission to edit it."}, status=status.HTTP_404_NOT_FOUND)

    name = request.data.get('name', strategy.name)
    description = request.data.get('description', strategy.description)
    parameters = request.data.get('parameters', strategy.parameters)

    if not name or not description:
        return Response({"detail": "Name and description are required."}, status=status.HTTP_400_BAD_REQUEST)

    strategy.name = name
    strategy.description = description
    strategy.parameters = parameters
    strategy.save()

    return Response({"message": "Strategy updated successfully!"}, status=status.HTTP_200_OK)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for handling 401 and 403 errors with custom messages.
    """
    response = exception_handler(exc, context)

    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            "error": "Authentication credentials were not provided or are invalid.",
            "detail": "Please include a valid token in the Authorization header."
        }

    elif response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            "error": "Permission Denied.",
            "detail": "You do not have the necessary permissions to perform this action."
        }

    return response
