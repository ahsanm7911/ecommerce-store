from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Product, ProductVariant, Color, Stock, Order, OrderItem, ConfirmedOrder, ShippingAddress, RefundPolicy, ClientEnquiry, CustomerReview
from accounts.models import Address
from django.http import JsonResponse, HttpResponse
from django.contrib.sites.models import Site
from django.views.decorators.http import require_GET
from django.core import serializers
from .utils import *  
from unrols.settings import USE_S3
from decouple import config
import json
# Create your views here.
# SEO VIEWS

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin",
        "Disallow: /cart", 
        "Disallow: /checkout",
        "Sitemap: https://unrols.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


    
def test(request):
    context = {}
    product = Product.objects.get(id=2)
    variants = ProductVariant.objects.filter(product=product)
    print(variants)
    context = {
        'product': product,
        'variants': variants,
    }
    return render(request, 'test.html', context)

def home(request):
    context = {}
    page = "Home"
    products = []
    sunglasses = []
    watches = []
    for product in Product.objects.all():
        variant = ProductVariant.objects.filter(product=product)[0]
        products.append(variant)
    
    try:
        watch_category = Category.objects.get(slug='watch')
    except Category.DoesNotExist:
        watch_category = None

    try:
        sunglasses_category = Category.objects.get(slug='sunglasses')
    except Category.DoesNotExist:
        sunglasses_category = None


    for product in Product.objects.filter(category__slug='watch'):
        variant = ProductVariant.objects.filter(product=product)[0]
        watches.append(variant)

    for product in Product.objects.filter(category__slug='sunglasses'):
        variant = ProductVariant.objects.filter(product=product)[0]
        sunglasses.append(variant)


    context = {
        'page': page,
        'products': products,
        'watches_category': watch_category,
        'sunglasses_category': sunglasses_category,
        'watches': watches,
        'sunglasses': sunglasses
    }
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
    main_product = Product.objects.get(category__slug=cat, slug=slug)
    variants = ProductVariant.objects.filter(product=main_product)
    bannerImage = variants[0].imageURL

    domain_name = request.get_host()
    product_link = domain_name + main_product.get_absolute_url()

    products_with_first_variant = []
    products = Product.objects.filter(category__slug=cat)

    for product in products:
        first_variant = product.productvariant_set.first()
        products_with_first_variant.append((product, first_variant))


    context = {
        'main_product': main_product,
        'variants': variants,
        'bannerImage': bannerImage,
        'product_link': product_link,
        'products_with_first_variant': products_with_first_variant
    }

    return render(request, 'core/product.html', context)

def lookbook(request):
    page = 'Lookbook'
    context = {}
    try:
        recommended_products = Product.objects.filter(stock=True)[:4]
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

        variantId = request.POST.get('product_id')
        action = request.POST.get('action')
        try:
            product =  ProductVariant.objects.get(id=variantId)
        except Product.DoesNotExist:
            product = None


        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

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
            product = ProductVariant.objects.get(id=id)
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
                get_product = ProductVariant.objects.get(id=i)
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
    # recommeded_products = Product.objects.filter(stock=True)[:4]
    if request.user.is_authenticated: # cart functionality for logged in user
        customer = request.user
        context = update_cart(customer)
    else:                               # cart functionality for guest user
        context = get_cart_data(request)
        # data to send as response for ajax
    # context['recommended_products'] = recommeded_products
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
    page = 'About'
    context = {}
    context['page'] = page
    return render(request, 'core/about.html', context)
