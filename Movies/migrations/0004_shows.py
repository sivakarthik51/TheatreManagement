# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-06 15:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0003_auto_20161106_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_time', models.DateTimeField(default=datetime.datetime(2016, 11, 6, 21, 14, 31, 366000))),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movies.Movie')),
            ],
        ),
    ]
