# Generated by Django 3.2.12 on 2022-04-06 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='modify_date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
