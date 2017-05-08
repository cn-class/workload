#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from django.utils.timezone import datetime

from .models import Support

class SupportForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Support.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	support_list = forms.ChoiceField(
			choices = ( 
				(u'อาจารย์ที่ปรึกษา','อาจารย์ที่ปรึกษา'),
				(u'อาจารย์ที่ปรึกษากิจกรรม','อาจารย์ที่ปรึกษากิจกรรม'),
				(u'ผู้ประสารงานดูแลนักศึกษาแลกเปลี่ยน','ผู้ประสารงานดูแลนักศึกษาแลกเปลี่ยน'),
				(u'ผู้ดูแลห้องปฏิบัติการ','ผู้ดูแลห้องปฏิบัติการ'),
				(u'ผู้ประสานงานวิชาฝึกงาน','ผู้ประสานงานวิชาฝึกงาน'),
				(u'ประธาน/กรรมการ/เลขานุการร่างหลักสูตร','ประธาน/กรรมการ/เลขานุการร่างหลักสูตร'),
				(u'เปิดซอง','เปิดซอง'),
				(u'ตรวจรับ','ตรวจรับ'),
				),
			label = "รายการ",
			widget = forms.RadioSelect,
			initial = u'อาจารย์ที่ปรึกษา',
			required = True,
		)

	degree = forms.ChoiceField(
			choices = ( 
				(u'ประธาน','ประธาน'),
				(u'กรรมการ','กรรมการ'),
				(u'อื่นๆ','อื่นๆ'),
				),
			label = "ระดับ",
			widget = forms.RadioSelect,
			initial = u'ประธาน',
			required = True,
		)

	kind = forms.ChoiceField(
			choices = ( 
				(u'ในคณะ','ในคณะ'),
				(u'นอกคณะ','นอกคณะ'),
				),
			label = "ประเภท",
			widget = forms.RadioSelect,
			initial = u'ในคณะ',
			required = True,
		)


	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(SupportForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.layout = Layout(

				Field('support_list'),
				Field('degree',),
				Field('kind',),
				Field('comment',),
				Div(
					Submit('submit','Submit'),
					style='text-align:center;'
					)
		)

	class Meta:
		model = Support
		fields = [
						"support_list",
						"degree",
						"kind",
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
		model = Support
		fields = [
					"year",
				]