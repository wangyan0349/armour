# Generated by Django 2.2 on 2019-09-05 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0029_keypoint_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keypoint',
            options={'ordering': ['point'], 'verbose_name': 'Key Point', 'verbose_name_plural': 'Key Points'},
        ),
        migrations.AlterModelOptions(
            name='keypointoption',
            options={'ordering': ['option'], 'verbose_name': 'Key Point Option', 'verbose_name_plural': 'Key Point Options'},
        ),
    ]
