# Generated by Django 2.2 on 2020-04-21 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0126_auto_20200421_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='corrective',
            field=models.TextField(max_length=2000, null=True, verbose_name='Actions to be taken'),
        ),
    ]
