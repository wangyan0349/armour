# Generated by Django 2.2 on 2020-02-03 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0095_auto_20200203_0430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sourcenc',
            options={'ordering': ['default'], 'verbose_name': 'NC Sources', 'verbose_name_plural': 'NC Sources'},
        ),
    ]
