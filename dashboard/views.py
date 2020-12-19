from django.shortcuts import render, redirect
from django.http import HttpResponse


def dashboard(request):
    user = request.user
    if user.is_authenticated:
        return redirect('main', request.user.username)
    else:
        return render(request, 'dashboard/landing_page.html')

