# Generated by Django 2.2 on 2019-05-19 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20190516_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
