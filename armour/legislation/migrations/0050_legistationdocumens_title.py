# Generated by Django 2.2 on 2019-09-18 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0049_legistationdocumens'),
    ]

    operations = [
        migrations.AddField(
            model_name='legistationdocumens',
            name='title',
            field=models.CharField(max_length=300, null=True, verbose_name='Title'),
        ),
    ]
