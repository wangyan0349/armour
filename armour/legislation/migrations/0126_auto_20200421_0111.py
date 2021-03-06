# Generated by Django 2.2 on 2020-04-21 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('legislation', '0125_version_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nccompleted', to=settings.AUTH_USER_MODEL, verbose_name='Identified by'),
        ),
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='completeddate',
            field=models.DateField(null=True, verbose_name='Completion date'),
        ),
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='identified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ncidentified', to=settings.AUTH_USER_MODEL, verbose_name='Identified by'),
        ),
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='priority',
            field=models.CharField(choices=[(1, 'Low'), (0, 'Medium'), (0, 'High')], default=1, max_length=15, verbose_name='Priority'),
        ),
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ncreviewed', to=settings.AUTH_USER_MODEL, verbose_name='Identified by'),
        ),
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='revieweddate',
            field=models.DateField(null=True, verbose_name='Review date'),
        ),
    ]
