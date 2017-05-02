#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timezone import now


class Teaching(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	subject_ID = models.CharField(max_length=10)
	subject = models.CharField(max_length=120)
	ratio = models.IntegerField()
	num_of_lecture = models.IntegerField()
	num_of_lab = models.IntegerField()
	program_ID = models.CharField(max_length=120)
	num_of_student = models.IntegerField()
	ratio_of_score = models.CharField(max_length=10) 
	comment = models.TextField(blank=True)
	date = models.DateTimeField(default=now,editable=True)

	@property
	def get_year(self):
		return self.date.strftime('%Y')




