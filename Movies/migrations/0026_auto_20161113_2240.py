# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-13 22:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0025_auto_20161113_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]