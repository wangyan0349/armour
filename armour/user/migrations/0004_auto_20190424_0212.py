# Generated by Django 2.2 on 2019-04-24 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190424_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='Username'),
        ),
    ]