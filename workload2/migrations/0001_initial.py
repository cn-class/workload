# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 15:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thesis_name', models.CharField(max_length=120)),
                ('ratio', models.IntegerField()),
                ('degree', models.CharField(max_length=120)),
                ('program_ID', models.CharField(max_length=120)),
                ('comment', models.TextField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
