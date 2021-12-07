# Generated by Django 2.2 on 2019-09-10 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0037_auto_20190910_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='assigned',
            field=models.TextField(max_length=2000, null=True, verbose_name='Assigned to'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='completion',
            field=models.TextField(max_length=2000, null=True, verbose_name='Completion date & by whom'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='containment',
            field=models.TextField(max_length=2000, null=True, verbose_name='Containment actions'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='corrective',
            field=models.TextField(max_length=2000, null=True, verbose_name='Corrective actions'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='cost',
            field=models.TextField(max_length=2000, null=True, verbose_name='Cost of nonconformance'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='identified',
            field=models.TextField(max_length=2000, null=True, verbose_name='Identified by'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='reviewed',
            field=models.TextField(max_length=2000, null=True, verbose_name='Reviewed and closed out by'),
        ),
        migrations.AlterField(
            model_name='legistationnonconformanceresponse',
            name='root',
            field=models.TextField(max_length=2000, null=True, verbose_name='Root cause'),
        ),
    ]
