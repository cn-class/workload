# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-30 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0007_teaching_subject_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaching',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
