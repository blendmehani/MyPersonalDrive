# Generated by Django 3.1.3 on 2021-02-09 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210126_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='file',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
