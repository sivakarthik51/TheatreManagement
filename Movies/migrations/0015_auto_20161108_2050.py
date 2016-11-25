# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-08 15:20
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Movies', '0014_auto_20161108_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='show',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 20, 50, 10, 55000)),
        ),
    ]
