# Generated by Django 2.2 on 2019-12-16 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0036_company_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo'),
        ),
    ]
