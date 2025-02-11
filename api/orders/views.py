from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from decimal import Decimal
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated

# Retrieve orders for the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
# Create a new order for the logged-in user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_create(request):
    data = request.data
    data['user'] = request.user.id  # Ensure the user is passed correctly

    data['action'] = data.get('action', '').upper()
    if data['action'] not in ['BUY', 'SELL']:
        return Response({'detail': 'Invalid action. Must be BUY or SELL.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        order = serializer.save(user=request.user)  # Explicitly set the user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve a specific order for the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_retrieve(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found or does not belong to you.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)
# Update the status of an order for the logged-in user
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_update_status(request, pk):
    from django.utils import timezone

    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found or does not belong to you.'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if new_status:
        new_status = new_status.upper()
        valid_statuses = ['PENDING', 'COMPLETED', 'CANCELED']
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

# Update take profit and stop loss for the logged-in user
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_update_tp_sl(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found or does not belong to you.'}, status=status.HTTP_404_NOT_FOUND)

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

# Update the PnL for an order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_update_pnl(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found or does not belong to you.'}, status=status.HTTP_404_NOT_FOUND)

    current_price = request.data.get('current_price')
    if current_price is not None:
        try:
            current_price = Decimal(current_price)
        except Exception:
            return Response({'detail': 'Invalid current price.'}, status=status.HTTP_400_BAD_REQUEST)

        pnl = current_price - order.entry_price
        if order.action == 'SELL':
            pnl = order.entry_price - current_price
        
        if order.take_profit and current_price >= order.take_profit:
            pnl = order.take_profit - order.entry_price
        elif order.stop_loss and current_price <= order.stop_loss:
            pnl = order.stop_loss - order.entry_price

        order.pnl = pnl
        order.save()
        return Response({'PnL': str(pnl)}, status=status.HTTP_200_OK)

    return Response({'detail': 'Current price is required for PnL calculation.'}, status=status.HTTP_400_BAD_REQUEST)

# Delete an order
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def order_delete(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found or does not belong to you.'}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

# Get net profit
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def net_profit(request):
    total_pnl = Order.objects.filter(user=request.user).aggregate(total_pnl=Sum('pnl'))['total_pnl']
    total_pnl = total_pnl if total_pnl is not None else Decimal('0.00')

    return Response({'net_profit': str(total_pnl)}, status=status.HTTP_200_OK)
