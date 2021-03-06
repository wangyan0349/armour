# Generated by Django 2.2 on 2020-07-03 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0154_auto_20200703_0832'),
        ('company', '0063_auto_20200622_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='discount',
            field=models.FloatField(editable=False, null=True, verbose_name='Discount'),
        ),
        migrations.AddField(
            model_name='payments',
            name='discount_code',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discountpayments', to='legislation.DiscountCodes', verbose_name='Discount code'),
        ),
        migrations.AddField(
            model_name='payments',
            name='discount_size',
            field=models.PositiveIntegerField(editable=False, null=True, verbose_name='Size [%]'),
        ),
    ]
