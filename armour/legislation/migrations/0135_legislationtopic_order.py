# Generated by Django 2.2 on 2020-05-06 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0134_question_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislationtopic',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Order'),
        ),
    ]
