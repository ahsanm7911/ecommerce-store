from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Account, Address, Newsletter
from core.models import ConfirmedOrder, Order, OrderItem
from django.http import HttpResponse, JsonResponse
from colorama import Fore

# Create your views here.

def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        error = ""
        # Validation checks
        if first_name == '' or last_name == '' or email == '' or password == '' or confirm_password == '':
            message = "Please fill all the required fields."
            return JsonResponse({'response': {'signal': 'err', 'message' : message}})
        
        if Account.objects.filter(email=email).exists():
            message = "Another account already exists with this email address."
            return JsonResponse({'response': {'signal': 'err', 'message' : message}})


        if len(password) < 8:
            message = "Your password must be consist of atleast 8 characters."
            return JsonResponse({'response': {'signal': 'err', 'message' : message}})


        
        if password != confirm_password:
            message = "Passwords donot match."
            return JsonResponse({'response': {'signal': 'err', 'message' : message}})

        

        new_user = Account.objects.create_user(email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        message = "You are registered successfully."
        return JsonResponse({'response': {'signal': 'success', 'message' : message}})

        # Display success message

        return redirect('login')
    
    return render(request, 'accounts/signup.html')

def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            message = "You are logged in successfully."
            return JsonResponse({'response': {'signal': 'success', 'message' : message}})
        else:
            message = "Invalid Email or Password."
            return JsonResponse({'response': {'signal': 'err', 'message': message}})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def reset_password(request):
    return render(request, 'accounts/reset_password.html')

def myaccount(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    orders = ConfirmedOrder.objects.filter(user=request.user)
    address_count = Address.objects.filter(user=request.user).count()
    context['orders'] = orders
    context['address_count'] = address_count
    return render(request, 'accounts/account.html', context)

def addresses(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    context = {}
    addresses = Address.objects.filter(user=request.user)
    context['addresses'] = addresses
    return render(request, 'accounts/addresses.html', context)

def add_address(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    message = ''
    if request.method == 'POST':
        is_default = ''
        full_name = request.POST.get('full_name')
        street = request.POST.get('street')
        city  = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        is_default = request.POST.get('is_default')

        if full_name == '' or street == '' or city == '' or phone == '':
            message = "Please fill all the mandatory fields."
            return JsonResponse({'response': {'signal' : 'err', 'message' : message}})
        
        new_address = Address.objects.create(user=request.user, full_name=full_name, street=street, city=city, country=country, postal_code=postal_code, phone=phone, is_default=is_default)
        new_address.save()
        message = 'Your address has been added.'
        return JsonResponse({'response': {'signal' : 'success', 'message' : message}})

    return render(request, 'accounts/add_address.html')

def edit_address(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = Address.objects.get(id=address_id)
    context['address'] = address
    return render(request, 'accounts/edit_address.html', context)

def edit_address_done(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        full_name = request.POST.get('full_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        is_default = request.POST.get('is_default')

        get_address = Address.objects.get(id=address_id)
        get_address.full_name = full_name
        get_address.street = street
        get_address.city = city
        get_address.country = country
        get_address.postal_code = postal_code
        get_address.phone = phone 
        get_address.is_default = is_default
        get_address.save()

        return redirect('addresses')

    return HttpResponse("Address updated.")

def delete_address(request):
    if request.method == 'POST':
        id_address = request.POST.get('address_id')
        address = Address.objects.get(id=id_address)
        address.delete()
        return JsonResponse({'message': 'Address deleted successfullly.'})


def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            newsletter = Newsletter.objects.get_or_create(email=email)
            # newsletter.save()
            message = "Thanks for subscribing to our newsletter."
            print(f'{email} added to newsletter.', Fore.GREEN)
        except Exception as e:
            message = "There was some error adding your email to our newsletter."
            print(e, Fore.RED)
        return HttpResponse(message)