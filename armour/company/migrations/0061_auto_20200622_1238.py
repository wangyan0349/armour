# Generated by Django 2.2 on 2020-06-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0060_auto_20200622_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='stripe_charge_id',
            field=models.CharField(editable=False, max_length=1000, null=True, verbose_name='Charge ID'),
        ),
    ]
