# Generated by Django 2.2 on 2020-05-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0052_auto_20200508_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='billzipcode',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Post code'),
        ),
        migrations.AlterField(
            model_name='company',
            name='zipcode',
            field=models.CharField(max_length=20, verbose_name='Post code'),
        ),
    ]
