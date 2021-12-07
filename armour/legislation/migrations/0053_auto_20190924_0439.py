# Generated by Django 2.2 on 2019-09-24 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0052_legislation_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legistationtopicsresponse',
            options={'ordering': ['legtopic__title'], 'verbose_name': 'Legislation topic response', 'verbose_name_plural': 'Legislation topic responses'},
        ),
        migrations.AlterField(
            model_name='legistationtopicsresponse',
            name='response',
            field=models.IntegerField(blank=True, choices=[(1, 'Full Compliance'), (0, 'No Compliance'), (2, 'Partial Compliance')], null=True),
        ),
    ]