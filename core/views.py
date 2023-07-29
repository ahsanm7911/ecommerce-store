from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Product, ProductImage, Order, OrderItem, ConfirmedOrder, ShippingAddress, RefundPolicy, ClientEnquiry, CustomerReview
from accounts.models import Address
from django.http import JsonResponse
from django.core import serializers
from .utils import *  
import json
# Create your views here.

def test(request):
    products = ProductImage.objects.filter(product__slug='rolex-watch')
    product_name = products[0].product.name
    product_price = products[0].product.price
    context = {}
    context['products'] = products
    context['product_name'] = product_name
    context['product_price'] = product_price
    return render(request, 'test.html', context)

def home(request):
    context = {}
    page = "Home"
    try:
        products = Product.objects.all()[:4]
    except Product.DoesNotExist:
        products = None
    try:
        watches = Product.objects.filter(category__slug='watches').order_by('created_at')
    except:
        watches = None
    try:
        sunglasses = Product.objects.filter(category__slug='sunglasses').order_by('-created_at')
    except:
        sunglasses = None
    try:
        watches_category = Category.objects.get(slug='watches').slug
    except:
        watches_category = None
    try:
        sunglasses_category = Category.objects.get(slug='sunglasses').slug
    except:
        sunglasses_category = None
    reviews = CustomerReview.objects.all()

    context['products'] = products
    context['watches'] = watches
    context['sunglasses'] = sunglasses
    context['watch_category'] = watches_category
    context['sunglass_category'] = sunglasses_category
    context['reviews'] = reviews
    context['page'] = page
    return render(request, 'core/index.html', context)

def products(request, slug):
    page = slug
    context = {}
    try:
        products = Product.objects.filter(category__slug=slug)
    except:
        products = None
    try:        
        paginator = Paginator(products, 8)
    except:
        pass
    
    category = slug
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    product_count = products.count()
    context['page_obj'] = page_obj
    context['product_count'] = product_count
    context['category'] = category
    context['page'] = page

    return render(request, 'core/products.html', context)

def product(request, cat, slug):
    context = {}

    try: 
        product = Product.objects.get(category__slug=cat, slug=slug)
    except Product.DoesNotExist:
        product = None

    try:    
        recommended_products = Product.objects.all().exclude(id=product.id)[:4]
        images = ProductImage.objects.filter(product=product)

        product_name = product.name
        product_price = product.price
        product_url = f'www.unrols.com/products/{product.category.slug}/{product.slug}/'
        product_colors = product.color.split(':')
        context['product_id'] = product.id
        context['product_name'] = product_name
        context['product_price'] = product_price
        context['primary_image'] = product.image
        context['product_url'] = product_url
        context['product_colors'] = product_colors
        context['product_desc'] = product.description
        context['product'] = product
        context['images'] = images
        page = product_name
        context['page'] = page

        context['recommended_products'] = recommended_products
    except:
        pass

    return render(request, 'core/product.html', context)

def lookbook(request):
    page = 'Lookbook'
    context = {}
    try:
        recommended_products = Product.objects.all()[:4]
    except:
        recommended_products = None
    try:   
        category = recommended_products[0].category.slug
    except:
        category = None

    context['recommended_products'] = recommended_products
    context['category'] = category
    context['page'] = page

    return render(request, 'core/lookbook.html', context)

def add_to_cart(request):
    if request.method == 'POST':

        id_product = request.POST.get('product_id')
        action = request.POST.get('action')
        color = request.POST.get('color')
        try:
            product =  Product.objects.get(id=id_product)
        except Product.DoesNotExist:
            product = None

        print('Color:', color)

        if color in product.color.split(':'):
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, color=color)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if action == 'delete':
            orderItem.delete()


        if orderItem.quantity <= 0:
            orderItem.delete()

        context = update_cart(customer)
        qty = orderItem.quantity
        context['qty'] = qty
        context['item_total'] = orderItem.get_item_total
        context.pop('items')
        print(context)
        return JsonResponse(context, safe=False)
    
def unauth_cart(request):
    context = {}
    if request.method == 'POST':
        id = request.POST.get('product_id')
        cart = json.loads(request.COOKIES['cart'])
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            product = None
        try: 
            item_total = 0
            item_total = product.price * cart[id]['quantity']
            context['item_total'] = item_total
            context['item_quantity'] = cart[id]['quantity']
        except KeyError:
            context['item_total'] = None
            context['item_quantity'] = None
        finally:
            order_total = 0
            for i in cart:
                get_product = Product.objects.get(id=i)
                product_total = get_product.price * cart[i]['quantity']
                order_total += product_total

            context['order_total'] = order_total
        return JsonResponse(context, safe=False)


def updating_cart_total(request):
    context = {}
    if request.method == 'POST':
        cart = json.loads(request.COOKIES['cart'])
        order_total = cart_total(cart)
        context['order_total'] = order_total
        return JsonResponse(context, safe=False)


def cart(request):
    page = 'Cart'
    context = {}
    recommeded_products = Product.objects.all()[:4]
    if request.user.is_authenticated: # cart functionality for logged in user
        customer = request.user
        context = update_cart(customer)
    else:                               # cart functionality for guest user
        context = get_cart_data(request)
        # data to send as response for ajax
    context['recommended_products'] = recommeded_products
    context['page'] = page
    return render(request, 'core/cart.html', context)

def process_checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        if request.user.is_authenticated:
            address_id = request.POST.get('address_id')
            print('Address id', address_id)
            try:
                address = Address.objects.get(id=address_id)
            except Address.DoesNotExist:
                address = None
            shipping_address = f'{address.full_name} , {address.phone}\n{address.street}, {address.city}, {address.country}\n{address.postal_code}.'

            order_details = ''
            order = Order.objects.get(customer=request.user, is_complete=False)
            for item in order.orderitem_set.all():
                order_details += f'{item.product.name} x {item.quantity} | Color: {item.color}\n'
            order_total = order.get_order_total
            
            new_order = ConfirmedOrder.objects.create(user=request.user, shippingAddress=shipping_address, order_details=order_details, bill=order_total, payment_method=payment_method)
            new_order.registered_user = True
            order.is_complete = True
            order.save()
            new_order.save()
        else:

            shipping_address = f'{full_name} , {phone}\n{street}, {city}, {country}\n{postal_code}.'
            
            cartData = get_cart_data(request)
            item_details = ''
            for i in cartData['items']:
                item_details += f'{i["product_name"]} x {i["product_quantity"]} | Color: {i["product_color"]}\n'
            order_total = cartData['order_total']
            order_details = str(item_details)
            new_order = ConfirmedOrder.objects.create(shippingAddress=shipping_address, order_details=order_details, bill=order_total, payment_method=payment_method)
            new_order.save()

    return JsonResponse(new_order.transaction_id, safe=False)

def checkout(request):
    page = 'Checkout'
    context = {}
    if request.user.is_authenticated:
        customer = request.user
        context = update_cart(customer)
        addresses = Address.objects.filter(user=customer)
        context['addresses'] = addresses
    else:
        context = get_cart_data(request)
    context['page'] = page
    
    return render(request, 'core/checkout.html', context)


def refund_policy(request):
    page = 'Refund Policy'
    context = {}
    try:
        refund_policy = RefundPolicy.objects.filter(is_active=True)
        context['refund_policy'] = refund_policy[0]
    except IndexError as e:
        print(e)
        context['refund_policy'] = e
    except RefundPolicy.DoesNotExist as e:
        print(e)
        refund_policy = None
        context['refund_policy'] = refund_policy
    context['page'] = page

    return render(request, 'core/refund_policy.html', context)

def shipping_policy(request):
    page = 'Shipping Details'
    context = {}
    try:
        shipping_policy = ShippingPolicy.objects.filter(is_active=True)
        context['shipping_policy'] = shipping_policy[0]
    except IndexError as e:
        print(e)
        context['shipping_policy'] = e
    except ShippingPolicy.DoesNotExist:
        shipping_policy = None
        context['shipping_policy'] = shipping_policy
    context['page'] = page

    return render(request, 'core/shipping_policy.html', context)

def store_policy(request):
    page = 'Policy'
    context = {}
    context['page'] = page

    return render(request, 'core/store_policy.html', context)

def contact(request):
    page = 'Contact'
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')

        enquiry = ClientEnquiry.objects.create(name=name, email=email, comment=comment)
        enquiry.save()
        message = "Your message have been submitted. We'll reach out to you shortly."
        return JsonResponse(message, safe=False)
    context['page'] = page
    return render(request, 'core/contact.html', context)

def about(request):
<<<<<<< HEAD
    page = 'About'
    context = {}
    context['page'] = page
    return render(request, 'core/about.html', context)
=======
    return render(request, 'core/about.html')
>>>>>>> f36632f135f280b8d173a16c6353f21ea9f9b812
