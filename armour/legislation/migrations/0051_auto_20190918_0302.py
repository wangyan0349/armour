# Generated by Django 2.2 on 2019-09-18 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0050_legistationdocumens_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegistationDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Title')),
                ('file', models.FileField(max_length=2000, upload_to='legislation/documents/%Y/%m/%d/', verbose_name='File')),
                ('uuid', models.UUIDField(editable=False, null=True)),
                ('legislation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legdocs', to='legislation.Legislation')),
            ],
            options={
                'verbose_name': 'Legislation position',
                'verbose_name_plural': 'Legislation positions',
            },
        ),
        migrations.DeleteModel(
            name='LegistationDocumens',
        ),
    ]
