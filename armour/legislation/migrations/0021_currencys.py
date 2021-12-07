# Generated by Django 2.2 on 2019-08-06 04:49

from django.db import migrations

def load_currency(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    s = Site.objects.all()
    s = s[0]

    Currency = apps.get_model("legislation", "Currency")
    Currency.objects.all().delete()

    h = Currency.objects.create(name="GBP", settings=s.site_settings,main=True)
    h = Currency.objects.create(name="EUR", settings=s.site_settings, main=False)


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0020_auto_20190806_0446'),
    ]

    operations = [
        migrations.RunPython(load_currency),
    ]
