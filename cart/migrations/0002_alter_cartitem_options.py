# Generated by Django 4.0.1 on 2022-01-20 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['-id']},
        ),
    ]
