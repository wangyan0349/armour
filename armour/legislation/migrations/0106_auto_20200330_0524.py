# Generated by Django 2.2 on 2020-03-30 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0105_auto_20200219_0138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Sector', 'verbose_name_plural': 'Sectors'},
        ),
    ]
