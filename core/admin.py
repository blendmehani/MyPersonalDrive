from django.contrib import admin
from .models import Directory, File, SharedFile

admin.site.register(Directory)
admin.site.register(File)
admin.site.register(SharedFile)