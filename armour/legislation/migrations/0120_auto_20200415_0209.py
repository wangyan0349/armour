# Generated by Django 2.2 on 2020-04-15 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0119_auto_20200414_0520'),
    ]

    operations = [
        migrations.AddField(
            model_name='keypoint',
            name='changed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Changed'),
        ),
        migrations.AddField(
            model_name='legislationtopic',
            name='changed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Changed'),
        ),
        migrations.AddField(
            model_name='question',
            name='changed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Changed'),
        ),
    ]
