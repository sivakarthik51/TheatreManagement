# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-08 14:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0013_auto_20161108_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='movie',
        ),
        migrations.AlterField(
            model_name='show',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 20, 22, 13, 992000)),
        ),
    ]
