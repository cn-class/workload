#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from django.utils.timezone import datetime

from .models import Document

class DocumentForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Document.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	subject_ID = forms.CharField(
			label = "รหัสวิชา",
			required = True,
		)

	subject_name = forms.CharField(
			label = "ชื่อวิชา",
			required = True,
		)

	assist_name = forms.CharField(
			label = "ชื่อผู้แต่งร่วม",
			required = True,
		)

	page = forms.IntegerField(
			label = "จำนวนหน้า",
			required = True,
		)


	ratio = forms.IntegerField(
			label = "สัดส่วนผลงาน(คิดเป็นร้อยละ)",
			required = True,
		)

	degree = forms.ChoiceField(
			choices = ( 
				(u'ผลงานวิชาการ','ผลงานวิชาการ'),
				(u'คู่มือปฏิบัติการ','คู่มือปฏิบัติการ'),
				(u'เอกสารประกอบการสอน','เอกสารประกอบการสอน'),
				(u'เอกสารคำสอน','เอกสารคำสอน'),
				(u'ตำราหรือหนังสือ','ตำราหรือหนังสือ'),
				),
			label = "ระดับ",
			widget = forms.RadioSelect,
			initial = u'ผลงานวิชาการ',
			required = False,
		)


	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(DocumentForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.layout = Layout(

				Field('subject_ID'),
				Field('subject_name'),
				Field('assist_name'),
				Field('page'),
				Field('ratio',),
				Field('degree',),
				Field('comment',),
				Div(
					Submit('submit','Submit'),
					style='text-align:center;'
					)
		)

	class Meta:
		model = Document
		fields = [
						"subject_ID",
						"subject_name",
						"assist_name",
						"page",
						"ratio",
						"degree",
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
		model = Document
		fields = [
					"year",
				]