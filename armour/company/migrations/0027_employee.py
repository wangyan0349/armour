# Generated by Django 2.2 on 2019-08-19 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0026_company_scope'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=400, verbose_name='Fist Name')),
                ('lname', models.CharField(max_length=400, verbose_name='Last name')),
                ('email', models.EmailField(max_length=400, null=True, verbose_name='Email')),
                ('postion', models.CharField(max_length=150, verbose_name='Position')),
                ('status', models.CharField(max_length=150, verbose_name='Status')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='company.Company')),
            ],
            options={
                'verbose_name_plural': 'Employees',
                'verbose_name': 'Employee',
            },
        ),
    ]
