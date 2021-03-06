# Generated by Django 3.2.12 on 2022-05-08 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0001_initial'),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wrapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='작성일자')),
                ('modify_date', models.DateTimeField(blank=True, null=True, verbose_name='수정일자')),
                ('title', models.CharField(max_length=50)),
                ('app_name', models.CharField(max_length=20)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('event', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('eventgroup', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.eventgroup')),
                ('post', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='작성일자')),
                ('modify_date', models.DateTimeField(blank=True, null=True, verbose_name='수정일자')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wrapper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.wrapper')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(verbose_name='작성일자')),
                ('modify_date', models.DateTimeField(blank=True, null=True, verbose_name='수정일자')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.reply')),
            ],
        ),
    ]
