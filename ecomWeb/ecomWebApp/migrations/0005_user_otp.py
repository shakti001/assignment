# Generated by Django 5.0.2 on 2024-03-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomWebApp', '0004_alter_user_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Otp',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]