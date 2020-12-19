from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegisterForm, LoginForm
from random import randint
from .models import User


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('main', request.user.username)

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('main', request.user.username)
    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, 'accounts/login.html', context)


def register_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('main', request.user.username)

    if request.POST:
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            birthdate = form.cleaned_data.get('birthdate')
            register = form.save(commit=False)
            year = birthdate.strftime('%Y')
            username = first_name.lower() + last_name.lower() + str(year)
            while User.objects.filter(username=username).exists():
                username = first_name.lower() + last_name.lower() + str(randint(1, 100000))
            register.username = username
            register.first_name = register.first_name.capitalize()
            register.last_name = register.last_name.capitalize()
            register.country = register.country.capitalize()
            register.city = register.city.capitalize()
            register.save()

            return redirect('login')
        else:
            form.initial = {
                "first_name": request.POST['first_name'],
                "last_name": request.POST['last_name'],
                "email": request.POST['email'],
                "gender": request.POST['gender'],
                "birthdate": request.POST['birthdate'],
                "country": request.POST['country'],
                "city": request.POST['city'],
                "phone_number": request.POST['phone_number']
            }
            context['register_form'] = form
    else:
        form = RegisterForm()
        context['register_form'] = form
    return render(request, 'accounts/register.html', context)


def logout_view(request, username):
    logout(request)
    return redirect('login')
