# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0004_auto_20170315_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaching',
            name='ratio_of_score',
            field=models.CharField(max_length=10),
        ),
    ]
