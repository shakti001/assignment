# Generated by Django 5.0.2 on 2024-03-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomWebApp', '0003_alter_user_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
