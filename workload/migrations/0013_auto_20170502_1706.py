# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-02 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0012_auto_20170502_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaching',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
