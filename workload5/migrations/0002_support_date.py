# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-01 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workload5', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
