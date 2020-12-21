from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin, Group


class MyUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'country')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login', 'password')
    filter_horizontal = ()
    list_filter = ('country', 'city', 'gender',)
    fieldsets = ()
    add_fieldsets = (
        ("All fields are required", {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'gender', 'email',
                       'country', 'city', 'phone_number', 'birthdate', 'password1', 'password2'),
        }),
    )


admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
