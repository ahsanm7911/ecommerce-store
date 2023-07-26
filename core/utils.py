from .models import *
import json

def get_cart_data(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    context = {}
    order_total = 0
    items = []
    for i in cart:
        try:
            product = {}
            get_product = Product.objects.get(id=i)
            item_total = (get_product.price * cart[i]['quantity'])
            get_product_image = get_product.image
            product['item_total'] = item_total
            product['product_image'] = get_product_image
            product['product_id'] = get_product.id
            product['product_name'] = get_product.name
            product['product_price'] = get_product.price
            product['product_quantity'] = cart[i]['quantity']
            product['product_color'] = cart[i]['color']
            items.append(product)
            order_total += item_total
        except:
            pass

    context['order_total'] = order_total
    context['items'] = items
    context['item_count'] = len(items)
    return context

def update_cart(customer):
    try:
        order = Order.objects.get(customer=customer, is_complete=False)
    except Order.DoesNotExist:
        order = None
    orderItems = OrderItem.objects.filter(order=order)
    items = []
    item_total = 0
    order_total = 0

    for item in orderItems:
        try:
            product = {}
            id = item.product.id
            get_product_image = Product.objects.get(id=id).image
            item_total = item.product.price * item.quantity
            order_total += item_total
            product['product_id'] = item.product.id
            product['product_name'] = item.product.name
            product['product_price'] = item.product.price
            product['product_image'] = get_product_image
            product['product_quantity'] = item.quantity
            product['product_color'] = item.color
            product['item_total'] = item_total
            items.append(product)
        except:
            pass
    context = {}
    context['items'] = items
    context['order_total'] = order_total
    context['item_count'] = orderItems.count()
    return context

def cart_total(cart):
    order_total = 0
    for i in cart:
        get_product = Product.objects.get(id=i)
        product_total = get_product.price * cart[i]['quantity']
        order_total += product_total
    return order_total
