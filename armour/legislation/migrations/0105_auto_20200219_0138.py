# Generated by Django 2.2 on 2020-02-19 01:38

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0104_auto_20200219_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keypoint',
            name='point',
            field=ckeditor.fields.RichTextField(max_length=10000, verbose_name='Key Point'),
        ),
    ]
