# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0014_remove_teaching_ratio_of_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.AlterField(
            model_name='teaching',
            name='program_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workload.Program'),
        ),
    ]
