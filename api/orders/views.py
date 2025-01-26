from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from decimal import Decimal
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated

# Order List (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# Order Creation (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Retrieve (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_retrieve(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

# Order Update Status (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_update_status(request, pk):
    from django.utils import timezone

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')  # Fetch 'status' from request data
    if new_status:
        new_status = new_status.upper()  # Convert status to uppercase for consistency
        valid_statuses = ['PENDING', 'COMPLETED', 'CANCELED']  # Example statuses; update based on your model
        if new_status in valid_statuses:
            order.status = new_status
            if new_status == 'COMPLETED':
                order.completed_at = timezone.now()
            elif new_status == 'CANCELED':
                order.canceled_at = timezone.now()
            order.save()
            return Response({'status': order.status}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'Invalid status. Valid statuses are: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'No status provided.'}, status=status.HTTP_400_BAD_REQUEST)

# Order Update Take Profit and Stop Loss (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_update_take_profit_stop_loss(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    take_profit = request.data.get('take_profit')
    stop_loss = request.data.get('stop_loss')

    if take_profit is not None:
        try:
            order.take_profit = Decimal(take_profit)
        except Exception:
            return Response({'detail': 'Invalid take profit value.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if stop_loss is not None:
        try:
            order.stop_loss = Decimal(stop_loss)
        except Exception:
            return Response({'detail': 'Invalid stop loss value.'}, status=status.HTTP_400_BAD_REQUEST)

    order.save()
    return Response({
        'take_profit': order.take_profit,
        'stop_loss': order.stop_loss
    }, status=status.HTTP_200_OK)

# Order Update PnL (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_update_pnL(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    current_price = request.data.get('current_price')
    if current_price is not None:
        try:
            current_price = Decimal(current_price)
        except Exception:
            return Response({'detail': 'Invalid current price.'}, status=status.HTTP_400_BAD_REQUEST)

        pnl = current_price - order.entry_price
        if order.take_profit and current_price >= order.take_profit:
            pnl = order.take_profit - order.entry_price
        elif order.stop_loss and current_price <= order.stop_loss:
            pnl = order.stop_loss - order.entry_price

        order.pnl = pnl
        order.save()
        return Response({'PnL': str(pnl)}, status=status.HTTP_200_OK)

    return Response({'detail': 'Current price is required for PnL calculation.'}, status=status.HTTP_400_BAD_REQUEST)

# Order Delete (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def order_delete(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def net_profit(request):
    # Calculate the sum of all PnL values (excluding None/null)
    total_pnl = Order.objects.aggregate(total_pnl=Sum('pnl'))['total_pnl']

    # If no orders or no PnL values, default to 0
    total_pnl = total_pnl if total_pnl is not None else Decimal('0.00')

    return Response({'net_profit': str(total_pnl)}, status=status.HTTP_200_OK)