#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from django.utils.timezone import datetime
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap3_datetime.widgets import DateTimePicker


from .models import Position

class PositionForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Position.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	position_name = forms.CharField(
			label = "รายการงานบริหาร",
			required = True,
		)

	# time_start = forms.CharField(
	# 		label = "วันที่เริ่มรับตำแหน่ง",
	# 		required = True,
	# 	)

	time_start = forms.DateField(
          widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))
		

	time_end = forms.CharField(
			label = "วันที่สิ้นสุดตำแหน่ง",
			required = True,
		)


	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(PositionForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.layout = Layout(

				Field('position_name'),
				Field('time_start',),
				Field('time_end',),
				Field('comment',),
				Div(
					Submit('submit','Submit'),
					style='text-align:center;'
					)
		)

	class Meta:
		model = Position
		fields = [
						"position_name",
						"time_start",
						"time_end",
						"comment",
			]		
		

class ChosenForm(forms.ModelForm):
	YEAR_CHOICES = []
 	for r  in range(2016,(datetime.today().year)+1):
 		YEAR_CHOICES.append((r,r))

 	year = forms.ChoiceField(
			choices = YEAR_CHOICES,
			initial=datetime.today().year,
			)
	
	def __init__(self, *args, **kwargs):

		super(ChosenForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.field_template = 'bootstrap3/layout/inline_field.html' 
		self.helper.form_class = 'form-inline'
		self.helper.form_id = 'chosen_sub'
		self.helper.layout = Layout(

				'year',
					Submit('submit','Submit'),
		)

	class Meta:
		model = Position
		fields = [
					"year",
				]