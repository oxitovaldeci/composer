# Generated by Django 3.2.3 on 2021-07-04 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
    ]
