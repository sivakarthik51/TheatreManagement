# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-13 22:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0023_auto_20161113_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]