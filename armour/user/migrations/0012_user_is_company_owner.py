# Generated by Django 2.2 on 2019-08-23 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_user_is_company_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_company_owner',
            field=models.BooleanField(default=False, verbose_name='Company owner'),
        ),
    ]