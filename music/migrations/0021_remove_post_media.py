# Generated by Django 3.2.3 on 2021-11-29 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0020_auto_20211119_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='media',
        ),
    ]
