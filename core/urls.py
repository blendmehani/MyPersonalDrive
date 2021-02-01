from django.urls import path
from core.views import (
    main,
    user_settings,
    delete_user,
    deactivate_user,
    create_directory,
    nested,
    upload_file,
    change_name,
    delete_file,
    empty_recycle_bin,
    recycle_bin,
    restore_all,
    restore_selected,
    permanently_delete_selected,
    share_file,
    shared_files,
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
    path('delete_file', delete_file, name='delete_file'),
    path('empty_recycle_bin', empty_recycle_bin, name='empty_recycle_bin'),
    path('recycle_bin', recycle_bin, name='recycle_bin'),
    path('restore_all', restore_all, name='restore_all'),
    path('restore_selected', restore_selected, name='restore_selected'),
    path('delete_permanently', permanently_delete_selected, name='permanently_delete_selected'),
    path('share_file', share_file, name='share_file'),
    path('shared_files', shared_files, name='shared_files'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='password_change'),
]
