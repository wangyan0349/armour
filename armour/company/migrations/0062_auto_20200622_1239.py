# Generated by Django 2.2 on 2020-06-22 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0061_auto_20200622_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='stripe_invoice_pdf',
            field=models.URLField(max_length=1000, null=True, verbose_name='Invoice PDF'),
        ),
    ]
