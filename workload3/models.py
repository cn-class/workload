#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timezone import now

# Create your models here.
class Research(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	research_name = models.CharField(max_length=120)
	assist_name = models.CharField(max_length=120)
	journal_name = models.CharField(max_length=120)
	year = models.IntegerField()
	ratio = models.IntegerField()
	degree = models.CharField(max_length=120)
	comment = models.TextField(blank=True)
	date = models.DateTimeField(default=now,editable=True)