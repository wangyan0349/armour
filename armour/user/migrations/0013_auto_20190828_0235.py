# Generated by Django 2.2 on 2019-08-28 02:35

from django.db import migrations

def set_owners(apps, schema_editor):
    User = apps.get_model("user", "User")
    User.objects.filter(company__isnull=False,is_company_admin=False).update(is_company_admin=True,is_company_owner=False)

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_is_company_owner'),
    ]

    operations = [
        migrations.RunPython(set_owners),
    ]
