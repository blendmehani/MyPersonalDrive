from django.contrib import admin
from .models import Requests
from django.utils.translation import ngettext
from django.contrib import messages
from django.core.mail import send_mail


class RequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'staff', 'is_new', 'is_registered', 'is_processed', 'is_finished',
                    'is_informed', 'request_date', 'finished_date', 'id')
    search_fields = ('id', 'full_name')
    readonly_fields = ('message', 'full_name', 'email', 'request_date', 'is_new', 'is_registered', 'staff', 'id')
    list_filter = ('is_new', 'is_registered', 'is_processed', 'is_finished', 'is_informed', 'request_date')
    list_display_links = ('full_name', 'email')
    fieldsets = [
        ['General information', {
            'fields': ['message', 'full_name', 'email', 'is_new', 'is_registered', 'request_date', 'staff', 'id']
        }],
        ['Change options', {
            'fields': [('is_processed', 'is_finished', 'is_informed'), 'finished_date']
        }]
    ]

    def make_processed(self, request, queryset):
        updated = queryset.update(is_new=False, is_processed=True, is_finished=False, is_informed=False)
        self.message_user(request, ngettext(
            '%d request was successfully changed to processing state.',
            '%d requests were successfully changed to processing state.',
            updated,
        ) % updated, messages.SUCCESS)

    make_processed.short_description = 'Change selected Requests to processing state'
    actions = [make_processed]

    def save_model(self, request, obj, form, change):
        obj.staff = request.user.email
        if 'send_email' in request.POST:
            result = Requests.objects.get(id=obj.id)
            obj.is_processed = result.is_processed
            obj.is_finished = result.is_finished
            obj.is_informed = result.is_informed

            text = f"""Dear {obj.full_name},

This email is related to the message that you contacted us in {obj.request_date}.
{request.POST['text_area']}

All the best,
MyPersonalDrive Team
            """
            send_mail(
                'Your request on MyPersonalDrive',
                text,
                'contact.mypersonaldrive@gmail.com',
                [obj.email],
                fail_silently=False,
            )
            if send_mail:
                self.message_user(request, f'Email has been sent successfully to {obj.email}')
        super().save_model(request, obj, form, change)

    change_form_template = 'admin/auth/request/request_form.html'

    def has_add_permission(self, request):
        return False


admin.site.register(Requests, RequestAdmin)
