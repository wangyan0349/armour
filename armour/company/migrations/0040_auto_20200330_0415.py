# Generated by Django 2.2 on 2020-03-30 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0039_auto_20200330_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='scope',
            field=models.TextField(blank=True, max_length=3000, null=True, verbose_name='Organisational scope'),
        ),
    ]
