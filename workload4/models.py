#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class Document(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	subject_ID = models.CharField(max_length=120)
	subject_name = models.CharField(max_length=120)
	assist_name = models.CharField(max_length=120)
	page = models.IntegerField()
	ratio = models.IntegerField()
	degree = models.CharField(max_length=120)
	comment = models.TextField()