from django import template
from core.models import Order, OrderItem
import json

register = template.Library()

def items_count(request):
    customer = request.user
    try:
        order = Order.objects.get(customer=customer, is_complete=False)
    except Order.DoesNotExist:
        order = None
    orderItems = OrderItem.objects.filter(order=order)
    return orderItems.count()

def items_count_guest(request):
    itemCount = 0
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    for i in cart:
        itemCount += 1
    return itemCount

def format_price(price):
    return "{:,.0f}".format(price)


register.filter('items_count', items_count)
register.filter('items_count_guest', items_count_guest)
register.filter('format_price', format_price)