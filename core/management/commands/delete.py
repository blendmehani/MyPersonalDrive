from django.core.management.base import BaseCommand
from core.models import Directory, File
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):

        deleted_directories = Directory.objects.filter(is_deleted=True,
                                                       date_created__lt=datetime.datetime.now()-datetime.timedelta(30))
        deleted_files = File.objects.filter(is_deleted=True, date_created__lt=datetime.datetime.now()-datetime.timedelta(30))

        if deleted_directories:
            print("Deleted Directories:")
            print("--------------------")
            for directory in deleted_directories:
                print(directory)
                directory.delete()
            print("--------------------")
        else:
            print('No Directories Deleted')
        if deleted_files:
            print("Deleted Files:")
            print("--------------------")
            for file in deleted_files:
                print(file)
                file.delete()
            print("--------------------")
        else:
            print('No Files Deleted')
