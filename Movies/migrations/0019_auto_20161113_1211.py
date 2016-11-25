# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-13 06:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0018_auto_20161109_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='theatre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Establishments.Theatre'),
        ),
        migrations.AlterField(
            model_name='show',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 13, 12, 11, 34, 707000)),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('show', 'seat_no')]),
        ),
    ]