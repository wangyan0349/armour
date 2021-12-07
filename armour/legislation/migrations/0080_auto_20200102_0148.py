# Generated by Django 2.2 on 2020-01-02 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0079_legistationnonconformanceresponse_ncdesc'),
    ]

    operations = [
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='desc',
            field=models.TextField(max_length=2000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='assigned',
            field=models.TextField(max_length=2000, null=True, verbose_name='Assigned to'),
        ),
    ]
