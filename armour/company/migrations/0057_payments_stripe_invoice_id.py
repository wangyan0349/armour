# Generated by Django 2.2 on 2020-06-22 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0056_auto_20200617_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='stripe_invoice_id',
            field=models.CharField(max_length=1000, null=True, verbose_name='Invoice ID'),
        ),
    ]