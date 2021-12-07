# Generated by Django 2.2 on 2020-07-17 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0158_auto_20200708_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='category',
            field=models.ManyToManyField(blank=True, to='legislation.Category', verbose_name='Sector'),
        ),
        migrations.AddField(
            model_name='document',
            name='locations',
            field=models.ManyToManyField(blank=True, to='legislation.Location', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='document',
            name='topics',
            field=models.ManyToManyField(blank=True, to='legislation.Topic', verbose_name='Topics'),
        ),
        migrations.AddField(
            model_name='guidance',
            name='category',
            field=models.ManyToManyField(blank=True, to='legislation.Category', verbose_name='Sector'),
        ),
        migrations.AddField(
            model_name='guidance',
            name='locations',
            field=models.ManyToManyField(blank=True, to='legislation.Location', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='guidance',
            name='topics',
            field=models.ManyToManyField(blank=True, to='legislation.Topic', verbose_name='Topics'),
        ),
    ]
