# Generated by Django 2.2 on 2019-05-09 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0016_auto_20190426_0511'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=400, verbose_name='Key Point')),
                ('comply', models.CharField(max_length=400, verbose_name='What you need to comply')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
            ],
            options={
                'verbose_name_plural': 'Key Points',
                'verbose_name': 'Key Point',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=2000, verbose_name='Title')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='legislation.Location')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='legislation.Topic')),
            ],
            options={
                'verbose_name_plural': 'Questions',
                'verbose_name': 'Question',
            },
        ),
        migrations.CreateModel(
            name='KeyPointOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=100, verbose_name='Option')),
                ('keyp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='koptions', to='legislation.KeyPoint')),
            ],
            options={
                'verbose_name_plural': 'Key Point Options',
                'verbose_name': 'Key Point Option',
            },
        ),
        migrations.AddField(
            model_name='keypoint',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kpoints', to='legislation.Question'),
        ),
    ]
