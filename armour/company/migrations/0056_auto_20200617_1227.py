# Generated by Django 2.2 on 2020-06-17 12:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0055_auto_20200617_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='tax',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='total',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total'),
        ),
    ]
