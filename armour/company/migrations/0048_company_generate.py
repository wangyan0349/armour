# Generated by Django 2.2 on 2020-04-30 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0047_auto_20200427_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='generate',
            field=models.BooleanField(default=True, verbose_name='Free'),
        ),
    ]
