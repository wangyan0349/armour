# Generated by Django 2.2 on 2020-01-16 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0085_auto_20200116_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='legistationnonconformanceresponse',
            name='verified',
            field=models.BooleanField(default=False, editable=False, verbose_name='Verified'),
        ),
        migrations.AddField(
            model_name='nonconformanceouterresponse',
            name='verified',
            field=models.BooleanField(default=False, editable=False, verbose_name='Verified'),
        ),
        migrations.AlterField(
            model_name='legislationtopiccomply',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]