from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import IGPost
from core.models import ConfirmedOrder, ProductVariant
from .serializers import IGPostSerializer, ConfirmedOrderSerializer
# Create your views here.

@api_view(['GET'])
def ig_feed(request):
    posts = IGPost.objects.all()
    serializer = IGPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_orders(request):
    orders = ConfirmedOrder.objects.all()
    all_orders = []
    for order in orders:
        order_data = {}
        full_name = order.shippingAddress.split('\n')[0]
        name = full_name.split(' ')[0] + ' ' + full_name.split(' ')[1][0].capitalize() + '.'
        item = order.order_details.split('\n')[0].split('|')[0].split(' x ')[0].strip()
        color = order.order_details.split('\n')[0].split('|')[1].split(':')[1].strip()
        print(item)
        print(color)
        try:
            item_image = ProductVariant.objects.get(product__name=item, color__name=color).thumbnail
        except ProductVariant.DoesNotExist:
            item_image = ''
        order_data = {
            'name': name,
            'item': item,
            'image': item_image
        }
        all_orders.append(order_data)
    return Response(all_orders)


