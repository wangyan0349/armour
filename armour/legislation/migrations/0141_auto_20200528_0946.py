# Generated by Django 2.2 on 2020-05-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0140_auto_20200522_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='no',
            field=models.PositiveIntegerField(default=1, verbose_name='No'),
        ),
        migrations.AddField(
            model_name='nonconformanceouterresponse',
            name='no',
            field=models.PositiveIntegerField(default=1, verbose_name='No'),
        ),
    ]
