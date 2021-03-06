# Generated by Django 2.2 on 2020-04-17 02:50

from django.db import migrations

def load_version(apps, schema_editor):
    LegislationVersion = apps.get_model("legislation", "LegislationVersion")
    Legislation = apps.get_model("legislation", "Legislation")
    h = LegislationVersion.objects.get(version='1.0.0')
    Legislation.objects.all().update(version=h)

class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0123_auto_20200415_2339'),
    ]

    operations = [
        migrations.RunPython(load_version),
    ]
