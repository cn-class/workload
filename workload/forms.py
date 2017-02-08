from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Teaching

class TeachingForm(forms.ModelForm):
	class Meta:
		model = Teaching
		fields = [
			"user",
			"subject",
			"ratio",
			"num_of_lecture",
			"num_of_lab",
			"program_ID",
			"num_of_student",
			"ratio_of_score",
			"comment",
		]
