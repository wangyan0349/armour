# Generated by Django 2.2 on 2019-08-06 00:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_auto_20190806_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=1000, null=True, verbose_name='City')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Price')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('validate', models.DateTimeField(verbose_name='Validation date')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paymentscc', to='company.Company')),
            ],
            options={
                'verbose_name': 'Payments',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
