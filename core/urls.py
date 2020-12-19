from django.urls import path
from core import views
from accounts.views import logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='main'),
    path('logout/', logout_view, name='logout'),
    path('settings/', views.user_settings, name='settings'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='password_change'),




]
