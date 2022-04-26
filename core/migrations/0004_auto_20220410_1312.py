# Generated by Django 3.2.12 on 2022-04-10 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20220407_0023'),
        ('core', '0003_wrapper_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wrapper',
            name='content',
        ),
        migrations.AddField(
            model_name='wrapper',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.post'),
        ),
    ]
