# Generated by Django 2.2 on 2019-10-30 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0066_auto_20191030_0249'),
        ('company', '0035_payments_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.ManyToManyField(blank=True, to='legislation.Category', verbose_name='Category'),
        ),
    ]