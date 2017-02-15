from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Teaching

class TeachingForm(forms.ModelForm):

	user = forms.ModelChoiceField(
        queryset=Teaching.objects.all(),
        widget=forms.HiddenInput())

	class Meta:
		model = Teaching
		exclude = ['user']
		fields = [
			"subject",
			"ratio",
			"num_of_lecture",
			"num_of_lab",
			"program_ID",
			"num_of_student",
			"ratio_of_score",
			"comment",
		]

class ExportForm(forms.ModelForm):
	user = forms.ModelChoiceField(
        queryset=Teaching.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}))

	class Meta:
		model = Teaching
		fields = ["user",]
	