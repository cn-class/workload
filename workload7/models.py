#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class Benefit(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	benefit_list = models.CharField(max_length=120)
	benefit_name = models.CharField(max_length=120)
	comment = models.TextField()