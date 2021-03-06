# Generated by Django 2.2 on 2019-09-10 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0035_sourcenc'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegistationNonConformanceResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('identified', models.TextField(max_length=2000, verbose_name='Identified by')),
                ('assigned', models.TextField(max_length=2000, verbose_name='Assigned to')),
                ('containment', models.TextField(max_length=2000, verbose_name='Containment actions')),
                ('completion', models.TextField(max_length=2000, verbose_name='Completion date & by whom')),
                ('root', models.TextField(max_length=2000, verbose_name='Root cause')),
                ('corrective', models.TextField(max_length=2000, verbose_name='Corrective actions')),
                ('cost', models.TextField(max_length=2000, verbose_name='Cost of nonconformance')),
                ('reviewed', models.TextField(max_length=2000, verbose_name='Reviewed and closed out by')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legislation.SourceNC')),
                ('topicreply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicnon', to='legislation.LegistationTopicsResponse')),
            ],
            options={
                'verbose_name_plural': 'NC',
                'verbose_name': 'NC',
            },
        ),
    ]
