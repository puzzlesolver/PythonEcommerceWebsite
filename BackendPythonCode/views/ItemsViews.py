from django.shortcuts import render
from BackendCode.models import Item, Review
from BackendCode.serializers import ItemSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def getItems(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Item.objects.filter(
        name__icontains=query).order_by('-timestamp')
    page = request.query_params.get('page')
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ItemSerializer(products, many=True)
    return Response({'items': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getSingleItem(request, pk):
    product = Item.objects.get(_id=pk)
    serializer = ItemSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getHighlyRatedItems(request):
    products = Item.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ItemSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createItem(request):
    user = request.user
    product = Item.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )
    serializer = ItemSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createItemReview(request, pk):
    user = request.user
    product = Item.objects.get(_id=pk)
    data = request.data
    # Let the user know that review for the item already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Review for this item already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # Ask the user to rate the item if there is no rating or rate is 0
    elif data['rating'] == 0:
        content = {'detail': 'Please rate'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # Once user inputs a review display message the review has been posted
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )
        reviews = product.review_set.all()
        product.reviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()
        return Response('Review Posted')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateItem(request, pk):
    data = request.data
    product = Item.objects.get(_id=pk)
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.availableInStock = data['availableInStock']
    product.category = data['category']
    product.description = data['description']
    product.save()
    serializer = ItemSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def uploadItemImage(request):
    data = request.data
    product_id = data['product_id']
    product = Item.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response('Image uploaded successfully')


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteItem(request, pk):
    product = Item.objects.get(_id=pk)
    product.delete()
    return Response('Item Deleted')



