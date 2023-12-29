# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=512)),
                ('year_started', models.IntegerField()),
            ],
            options={
                'db_table': 'custom_artist',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=512)),
                ('established_year', models.IntegerField()),
                ('website', models.URLField()),
            ],
            options={
                'db_table': 'custom_label',
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='label',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_artists', to='custom_app.Label'),
        ),
    ]
