# Generated by Django 3.2.3 on 2021-07-09 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210709_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='document_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id_card',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
