# Generated by Django 3.2.12 on 2022-04-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220410_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='wrapper',
            name='model_nm',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
