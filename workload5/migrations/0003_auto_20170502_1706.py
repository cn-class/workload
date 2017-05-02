# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-02 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workload5', '0002_support_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='support',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]