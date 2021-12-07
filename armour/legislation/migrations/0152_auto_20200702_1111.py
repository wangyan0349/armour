# Generated by Django 2.2 on 2020-07-02 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0151_auto_20200702_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcodes',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='discountcodes',
            name='multiple',
            field=models.BooleanField(default=False, verbose_name='Multiple-use'),
        ),
    ]