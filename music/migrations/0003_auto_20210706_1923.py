# Generated by Django 3.2.3 on 2021-07-06 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_musicstyle_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='musician',
            options={'verbose_name': 'Músico', 'verbose_name_plural': 'Músicos'},
        ),
        migrations.AlterField(
            model_name='album',
            name='musician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.musician', verbose_name='Músico'),
        ),
    ]
