# Generated by Django 4.2.1 on 2023-06-05 11:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot_ema', '0008_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phoneNumber',
            field=models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
