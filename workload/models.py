#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

class Teaching(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	subject = models.CharField(max_length=120)
	ratio = models.IntegerField()
	num_of_lecture = models.IntegerField()
	num_of_lab = models.IntegerField()

	program_choice = (
			('1','ภาคปกติ'),
			('2','TEP/TEPE'),
			('3','AUTO'),
		)

	program_ID = models.CharField(max_length=120,choices=program_choice,default='1')


	num_of_student = models.IntegerField()
	ratio_of_score = models.IntegerField() 
	comment = models.TextField()

	def get_absolute_url(self):
		return reverse("workload:detail", kwargs={"id": self.id})