from django.urls import path
from core.views import (
    main,
    user_settings,
    delete_user,
    deactivate_user,
    create_directory,
    nested,
    upload_file,
    change_name
)
from accounts.views import logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main, name='main'),
    path('file/<dir_name>/', nested, name='nested'),
    path('logout/', logout_view, name='logout'),
    path('settings/', user_settings, name='settings'),
    path('delete/', delete_user, name='delete_user'),
    path('deactivate/', deactivate_user, name='deactivate_user'),
    path('create_directory/', create_directory, name='create_directory'),
    path('upload_file/', upload_file, name='upload_file'),
    path('change_name/', change_name, name='change_name'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='password_change'),
]
