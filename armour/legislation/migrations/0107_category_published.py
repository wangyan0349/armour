# Generated by Django 2.2 on 2020-04-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0106_auto_20200330_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='published',
            field=models.BooleanField(default=True, verbose_name='Published'),
        ),
    ]
