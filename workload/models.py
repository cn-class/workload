#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse


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
	comment = models.TextField()

	def __unicode__(self):
		return '%s %s %s %s' % (self.subject_ID,self.subject,self.program_ID,self.ratio_of_score)


	def get_absolute_url(self):
		return reverse("workload:list", kwargs={"id": self.id})