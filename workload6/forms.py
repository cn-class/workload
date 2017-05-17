#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from django.utils.timezone import datetime

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})



from .models import Position

class PositionForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Position.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	position_name = forms.ChoiceField(
			choices = ( 
				(u'รองคณบดี ผู้ช่วยคณะบดี หรือ หัวหน้าภาควิชา','รองคณบดี ผู้ช่วยคณะบดี หรือ หัวหน้าภาควิชา'),
				(u'รองหัวหน้าภาควิชา','รองหัวหน้าภาควิชา'),
				(u'ผู้อำนวยการบัณฑิตศึกษา','ผู้อำนวยการบัณฑิตศึกษา'),
				(u'ผู้อำนวยการโครงสร้างหลักสูตรในระดับปริญญาตรี','ผู้อำนวยการโครงสร้างหลักสูตรในระดับปริญญาตรี'),
				(u'ผู้อำนวยการศูนย์คอมพิวเตอร์และสารสนเทศ','ผู้อำนวยการศูนย์คอมพิวเตอร์และสารสนเทศ'),
				(u'รองผู้อำนวยการโครงสร้างหลักสูตรในระดับปริญญาตรี','รองผู้อำนวยการโครงสร้างหลักสูตรในระดับปริญญาตรี'),
				(u'รองผู้อำนวยการบัณฑิตศึกษา','รองผู้อำนวยการบัณฑิตศึกษา'),
				(u'รองผู้อำนวยการศูนย์คอมพิวเตอร์และสารสนเทศ','รองผู้อำนวยการศูนย์คอมพิวเตอร์และสารสนเทศ'),
				(u'ผู้อำนวยการ/หัวหน้าโครงการบริการสังคมโครงการปกติ','ผู้อำนวยการ/หัวหน้าโครงการบริการสังคมโครงการปกติ'),
				),
			label = "รายการงานบริหาร",
			required = True,
		)

	time_start = forms.DateField(
			label = "วันที่เริ่มรับตำแหน่ง",
			widget = DateInput(),
			required = True,
		)

	# time_start = forms.DateField(
 #        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
 #                                       "pickTime": False}))

		

	time_end = forms.DateField(
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