# Generated by Django 3.2.12 on 2022-04-15 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_wrapper_model_nm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wrapper',
            name='model_nm',
        ),
        migrations.RemoveField(
            model_name='wrapper',
            name='title',
        ),
    ]
