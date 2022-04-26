# Generated by Django 3.2.12 on 2022-04-04 14:54

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_wrapper_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='wrapper',
            name='content',
            field=picklefield.fields.PickledObjectField(default=1, editable=False),
            preserve_default=False,
        ),
    ]
