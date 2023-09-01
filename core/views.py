from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Product, ProductVariant, ProductImage, Color, Stock, Order, OrderItem, ConfirmedOrder, ShippingAddress, RefundPolicy, ClientEnquiry, CustomerReview
from accounts.models import Address
from django.http import JsonResponse, HttpResponse
from django.contrib.sites.models import Site
from django.views.decorators.http import require_GET
from django.core import serializers
from .utils import *  
import random
from unrols.settings import USE_S3
from decouple import config
import json
# Create your views here.
# SEO VIEWS


def maintenance(request):
    return render(request, 'maintenance_page.html')

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
    
    products = ProductVariant.objects.filter(display=True)
    mobile_banner_image = ProductVariant.objects.get(product__code='UNS-001', color__name='Black')
    desktop_banner_image = ProductVariant.objects.get(product__code='UNS-001',color__name='Black')
    print(mobile_banner_image)
    print(desktop_banner_image)

    try:
        watch_category = Category.objects.get(slug='watch')
    except Category.DoesNotExist:
        watch_category = None

    try:
        sunglasses_category = Category.objects.get(slug='sunglasses')
    except Category.DoesNotExist:
        sunglasses_category = None

    customer_reviews = CustomerReview.objects.all()

    watches = ProductVariant.objects.filter(product__category__slug='watches', display=True)
    sunglasses = ProductVariant.objects.filter(product__category__slug='sunglasses', display=True)

    context = {
        'page': page,
        'products': products,
        'watches_category': watch_category,
        'sunglasses_category': sunglasses_category,
        'watches': watches,
        'sunglasses': sunglasses,
        'mobile_banner_image': mobile_banner_image,
        'desktop_banner_image': desktop_banner_image,
        'reviews': customer_reviews
    }
    return render(request, 'core/index.html', context)

def products(request, slug):
    page = slug
    context = {}

    variants = ProductVariant.objects.filter(product__category__slug=slug, display=True)    
    product_count = len(variants)
    items_per_page = 8  
    try:        
        paginator = Paginator(variants, items_per_page)
    except:
        pass

    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None
    
    context = {
        'page': page,
        'page_obj': page_obj,
        'product_count': product_count
    }

    return render(request, 'core/products.html', context)

def product(request, cat, slug):
    context = {}
    main_product = Product.objects.get(category__slug=cat, slug=slug)
    variants = ProductVariant.objects.filter(product=main_product).order_by('-display')

    domain_name = request.get_host()
    product_link = domain_name + main_product.get_absolute_url()

    products_with_first_variant = []
    products = Product.objects.filter(category__slug=cat).exclude(id=main_product.id)

    product_images = ProductImage.objects.filter(product=main_product)
    page = main_product.name 

    products = ProductVariant.objects.filter(product__category__slug=cat, display=True).exclude(product=main_product)

    # Shipping details
    lead_time = timedelta(days=main_product.lead_time)
    current_date = date.today()

    # Define a list of holidays (dates) when shipping is not available 
    holidays = [date(2023, 12, 25), date(2023, 1, 1)] # Add your holidays here

    # Calculate the estimated shipping date considering weekends and holidays 
    shipping_date = current_date + lead_time
    while shipping_date.weekday() >= 5 or shipping_date in holidays:
        shipping_date += timedelta(days=1)

    

    context = {
        'page': page,
        'main_product': main_product,
        'variants': variants,
        'product_images': product_images,
        'product_link': product_link,
        'products': products,
        'shipping_date': shipping_date
    }

    return render(request, 'core/product.html', context)

def lookbook(request):
    page = 'Lookbook'
    context = {}

    products = []
    for product in Product.objects.all()[:4]:
        if product.productvariant_set.all().count() > 0:
            try:
                variant = product.productvariant_set.all()[0]
            except:
                variant = None
            products.append(variant)

    choices = []
    for i in ProductVariant.objects.all()[:11]:
        choices.append(i.id)
        
    

    image_one       = ProductVariant.objects.get(id=random.choice(choices))
    image_two       = ProductVariant.objects.get(id=random.choice(choices))
    image_three       = ProductVariant.objects.get(id=random.choice(choices))
    image_four       = ProductVariant.objects.get(id=random.choice(choices))
    image_five      = ProductVariant.objects.get(id=random.choice(choices))
    image_six       = ProductVariant.objects.get(id=random.choice(choices))
    image_seven       = ProductVariant.objects.get(id=random.choice(choices))
    image_eight       = ProductVariant.objects.get(id=random.choice(choices))
    image_nine       = ProductVariant.objects.get(id=random.choice(choices))
    image_ten       = ProductVariant.objects.get(id=random.choice(choices))
    image_eleven       = ProductVariant.objects.get(id=random.choice(choices))

    context = {
        'page': page,
        'products': products,
        'image_one': image_one,
        'image_two': image_two,
        'image_three': image_three,
        'image_four': image_four,
        'image_five': image_five,
        'image_six': image_six,
        'image_seven': image_seven,
        'image_eight': image_eight,
        'image_nine': image_nine,
        'image_ten': image_ten,
        'image_eleven': image_eleven,
    }

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

    variants = ProductVariant.objects.filter(display=True)[:4]

    if request.user.is_authenticated: # cart functionality for logged in user
        customer = request.user
        context = update_cart(customer)
    else:                               # cart functionality for guest user
        context = get_cart_data(request)
        # data to send as response for ajax
    context['page'] = page
    context['variants'] = variants
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

            shipping_address = f'{full_name}\n{phone}\n{street}, {city}, {country}\n{postal_code}.'
            
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
