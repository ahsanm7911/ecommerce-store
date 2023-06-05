from django.shortcuts import render, redirect
from .models import Email
# Create your views here.
def home(request):
    if request.method == "POST":
        email = request.POST['email']

        new_email = Email.objects.create(email=email)
        new_email.save()

        return redirect('/')

    return render(request, 'index.html')