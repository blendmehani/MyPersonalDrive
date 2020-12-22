from django.urls import path
from core.views import (
    main,
    user_settings,
    delete_user,
    deactivate_user
)
from accounts.views import logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main, name='main'),
    path('logout/', logout_view, name='logout'),
    path('settings/', user_settings, name='settings'),
    path('delete/', delete_user, name='delete_user'),
    path('deactivate', deactivate_user, name='deactivate_user'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='password_change'),

]
