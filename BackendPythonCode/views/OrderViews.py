from django.shortcuts import render
from rest_framework import status
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from BackendCode.models import Item, Order, OrderItem, ShippingAddress
from BackendCode.serializers import ItemSerializer, OrderSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'This order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'Items Unavailable'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Order creation
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxAdded'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        # Shipping address
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            zipCode=data['shippingAddress']['zipCode'],
            country=data['shippingAddress']['country'],
        )
        # Create order items. Set order to orderItem relationship
        for i in orderItems:
            product = Item.objects.get(_id=i['item'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=i['price'],
                image=product.image.url,
            )
            # Update the order in stock
            product.availableInStock -= item.quantity
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderPayment(request, pk):
    order = Order.objects.get(_id=pk)
    order.confirmPayment = True
    order.paymentTime = datetime.now()
    order.save()
    return Response('Your order has been paid')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderDelivery(request, pk):
    order = Order.objects.get(_id=pk)
    order.confirmDelivery = True
    order.deliveryTime = datetime.now()
    order.save()
    return Response('Your order has been delivered')
