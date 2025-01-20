from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Strategy

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_strategies(request):
    """Fetch all strategies for the authenticated user."""
    strategies = Strategy.objects.filter(user=request.user).values('id', 'name', 'description', 'parameters')
    return Response(list(strategies))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_strategy(request):
    """Create a new trading strategy."""
    name = request.data.get('name')
    description = request.data.get('description')
    parameters = request.data.get('parameters', {})
    if not name or not description:
        return Response({"detail": "Name and description are required"}, status=400)
    Strategy.objects.create(user=request.user, name=name, description=description, parameters=parameters)
    return Response({"message": "Strategy created successfully!"})
