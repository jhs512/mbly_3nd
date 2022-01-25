# Generated by Django 4.0.1 on 2022-01-11 02:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=100, verbose_name='마켓이름')),
                ('site_url', models.URLField(max_length=100, verbose_name='마켓사이트URL')),
                ('email', models.EmailField(max_length=100, verbose_name='마켓대표이메일')),
                ('master', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
