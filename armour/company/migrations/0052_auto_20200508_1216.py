# Generated by Django 2.2 on 2020-05-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0051_company_selectplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='selectplan',
            field=models.BooleanField(default=False, editable=False, verbose_name='Select plan'),
        ),
    ]
