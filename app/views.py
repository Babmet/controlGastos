from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import UserCreationForm

def home(request):
    return HttpResponse("¡Hola, mundo!")

def about(request):
    return HttpResponse("Acerca de nosotros")

def contact(request):
    return HttpResponse("Contáctanos")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u_email = form.cleaned_data.get('email')
            u_password = form.cleaned_data.get('password1')
            u_name = form.cleaned_data.get('name')
            u_lastname = form.cleaned_data.get('lastname')
            u_phone = form.cleaned_data.get('phone')
            u_address = form.cleaned_data.get('address')
            user = User.objects.create_user(
                email=u_email,
                password=u_password,
                name=u_name,
                lastname=u_lastname,
                phone=u_phone,
                address=u_address,
            )
            if user:
                messages.success(request, 'Your account has been created!')
            else:
                messages.error(request, 'There was an error creating your account.')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
