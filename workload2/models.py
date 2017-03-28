#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Thesis(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	thesis_name = models.CharField(max_length=120)
	ratio = models.IntegerField()
	degree = models.CharField(max_length=120)
	program_ID = models.CharField(max_length=120)
	comment = models.TextField()