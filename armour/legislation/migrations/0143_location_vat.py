# Generated by Django 2.2 on 2020-06-15 17:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0142_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='vat',
            field=models.PositiveIntegerField(default=23, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='VAT'),
        ),
    ]
