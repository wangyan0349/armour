# Generated by Django 2.2 on 2019-07-31 00:55

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20190731_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='billcountry',
            field=django_countries.fields.CountryField(max_length=2, null=True, verbose_name='Country'),
        ),
    ]