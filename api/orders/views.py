from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from decimal import Decimal

# Order List (GET)
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# Order Creation (POST)
@api_view(['POST'])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Retrieve (GET)
@api_view(['GET'])
def order_retrieve(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)

# Order Update Status (PUT)
@api_view(['PUT'])
def order_update_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Updating the order status
    status = request.data.get('status')
    if status:
        order.status = status
        order.save()
        return Response({'status': order.status}, status=status.HTTP_200_OK)

    return Response({'detail': 'No status provided'}, status=status.HTTP_400_BAD_REQUEST)

# Order Update Take Profit and Stop Loss (PUT)
@api_view(['PUT'])
def order_update_take_profit_stop_loss(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Update take_profit and stop_loss if provided
    take_profit = request.data.get('take_profit')
    stop_loss = request.data.get('stop_loss')

    if take_profit is not None:
        order.take_profit = take_profit
    
    if stop_loss is not None:
        order.stop_loss = stop_loss

    order.save()
    return Response({
        'take_profit': order.take_profit,
        'stop_loss': order.stop_loss
    }, status=status.HTTP_200_OK)

# Order Update PnL (PUT)
@api_view(['PUT'])
def order_update_pnL(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Calculate PnL based on current price, entry price, TP, and SL
    current_price = request.data.get('current_price')  # Assume this is passed in the request

    if current_price is not None:
        pnl = Decimal(current_price) - order.entry_price

        # Check if the current price hits TP or SL and adjust PnL accordingly
        if order.take_profit and Decimal(current_price) >= order.take_profit:
            pnl = Decimal(order.take_profit) - order.entry_price
        elif order.stop_loss and Decimal(current_price) <= order.stop_loss:
            pnl = Decimal(order.stop_loss) - order.entry_price

        return Response({'PnL': str(pnl)}, status=status.HTTP_200_OK)

    return Response({'detail': 'Current price is required for PnL calculation.'}, status=status.HTTP_400_BAD_REQUEST)

# Order Delete (DELETE)
@api_view(['DELETE'])
def order_delete(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
