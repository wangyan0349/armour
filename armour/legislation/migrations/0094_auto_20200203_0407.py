# Generated by Django 2.2 on 2020-02-03 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0093_auto_20200203_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='legistationtopicsresponse',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Default to Legal register'),
        ),
        migrations.AddField(
            model_name='legistationtopicsresponse',
            name='defaulto',
            field=models.BooleanField(default=False, verbose_name='Default to Outer NC'),
        ),
    ]
