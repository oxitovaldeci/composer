# Generated by Django 3.2.3 on 2021-10-11 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_auto_20211001_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='musician',
            name='artistic_name',
            field=models.CharField(default='', max_length=100, verbose_name='Nome Artístico'),
            preserve_default=False,
        ),
    ]