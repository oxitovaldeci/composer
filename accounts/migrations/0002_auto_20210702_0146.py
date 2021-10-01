# Generated by Django 3.2.3 on 2021-07-02 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='cpf',
            new_name='document_number',
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=None, verbose_name='Data de Nascimento'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=254, unique=True, verbose_name='E-mail'),
            preserve_default=False,
        ),
    ]
