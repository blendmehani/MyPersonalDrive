from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import sys
sys.setrecursionlimit(10000)


class Directory(models.Model):
    parent_dir_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dir_name = models.CharField(verbose_name='Directory Name', max_length=18)
    type = models.CharField(max_length=20, verbose_name='Type', default='directory')
    date_created = models.DateTimeField(verbose_name='Date Created', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Date Updated', auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Directories'

    def __str__(self):
        return self.dir_name

    def get_all_children(self, include_self=True):
        result = []
        if include_self:
            result.append(self)
        files = File.objects.filter(parent_dir_id=self)
        for file in files:
            result.append(file)
        for c in Directory.objects.filter(parent_dir_id=self):
            _result = c.get_all_children(include_self=True)

            if 0 < len(_result):
                result.extend(_result)
        return result


def upload_file_location(instance, filename):
    file_path = 'files/{username}/{filename}'.format(
        username=str(instance.user.username), filename=filename
    )
    return file_path


class File(models.Model):
    parent_dir_id = models.ForeignKey(Directory, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.CharField(verbose_name='File Name', max_length=18)
    type = models.CharField(max_length=20, verbose_name='Type', blank=True)
    file = models.FileField(verbose_name='File Path', upload_to=upload_file_location)
    date_created = models.DateTimeField(verbose_name='Date Created', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Date Updated', auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.file_name


@receiver(post_delete, sender=File)
def submission_delete(sender, instance, *args, **kwargs):
    instance.file.delete(False)


def pre_save_files_receiver(sender, instance, *args, **kwargs):
    file = instance.file.url
    print(file)
    if file.endswith('.pdf'):
        instance.type = 'pdf'
    elif file.endswith('.txt'):
        instance.type = 'txt'
    elif file.endswith(('.doc', '.docx')):
        instance.type = 'word'
    elif file.endswith(('xlsx', '.xlsm', '.xlsb', '.xltx', '.xltm', '.xls', '.xlt', '.xls', 'csv')):
        instance.type = 'excel'
    else:
        instance.type = 'image'


pre_save.connect(pre_save_files_receiver, sender=File)


class SharedFile(models.Model):
    shared_file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shared_from', on_delete=models.CASCADE)
    shared_to = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='shared_to', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name='Date Created', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Date Updated', auto_now=True)
