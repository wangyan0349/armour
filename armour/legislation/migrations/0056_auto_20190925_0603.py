# Generated by Django 2.2 on 2019-09-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0055_auto_20190924_0509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legistationtopicsresponse',
            options={'ordering': ['pos'], 'verbose_name': 'Legislation topic response', 'verbose_name_plural': 'Legislation topic responses'},
        ),
        migrations.AddField(
            model_name='legistationtopicsresponse',
            name='pos',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
