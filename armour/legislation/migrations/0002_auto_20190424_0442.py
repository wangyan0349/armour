# Generated by Django 2.2 on 2019-04-24 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('price', models.FloatField(null=True, verbose_name='Price')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='price',
            field=models.FloatField(null=True, verbose_name='Price'),
        ),
    ]
