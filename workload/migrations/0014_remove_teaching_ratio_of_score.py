# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 05:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0013_auto_20170502_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teaching',
            name='ratio_of_score',
        ),
    ]
