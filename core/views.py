from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UpdateUserForm
from accounts.models import User
from django.contrib.auth import logout


def main(request, username):
    user = request.user
    context = {}
    if user.is_authenticated:
        context['user_url'] = request.build_absolute_uri()
        return render(request, 'main_logic.html', context)

    return redirect('dashboard')


def user_settings(request, username):
    context = {}
    if request.POST:
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            update = form.save(commit=False)
            update.first_name = first_name.capitalize()
            update.last_name = last_name.capitalize()
            form.initial = {
                "first_name": request.POST['first_name'].capitalize(),
                "last_name": request.POST['last_name'].capitalize(),
                "email": request.POST['email'],
                "phone_number": request.POST['phone_number']
            }
            update.save()
            context['success_message'] = 'Data updated successfully.'
    else:
        form = UpdateUserForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "phone_number": request.user.phone_number
            }
        )
    context['update_user_form'] = form
    return render(request, 'user_settings.html', context)


def delete_user(request, username):
    user = User.objects.get(username=username)
    if request.POST:
        user.delete()
        return redirect('dashboard')
    context = {}
    return render(request, 'delete_user.html', context)


def deactivate_user(request, username):
    user = User.objects.get(username=username)
    if request.POST:
        user.is_active = 0
        user.save()
        return redirect('dashboard')
    context = {}
    return render(request, 'deactivate_user.html', context)


def create_directory(request, username):
    context = {}
    return render(request, 'actions/create_directory.html', context)