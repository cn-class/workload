#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from .models import Research

class ResearchForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Research.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	research_name = forms.CharField(
			label = "ชื่อผลงาน",
			required = True,
		)

	assist_name = forms.CharField(
			label = "ชื่อผู้ร่วมแต่ง",
			required = True,
		)

	journal_name = forms.CharField(
			label = "วารสารที่ตีพิมพ์",
			required = True,
		)

	year = forms.IntegerField(
			label = "ปีที่ตีพิมพ์",
			required = True,
		)


	ratio = forms.IntegerField(
			label = "สัดส่วนผลงาน(คิดเป็นร้อยละ)",
			required = True,
		)

	degree = forms.ChoiceField(
			choices = ( 
				(u'นานาชาติมี impact factor','นานาชาติมี impact factor'),
				(u'นานาชาติไม่มี impact factor','านาชาติไม่มี impact factor'),
				(u'ระดับชาติ มธ.','ระดับชาติ มธ.'),
				(u'วารสารนานาชาติที่อยู่ในข้อมูลสากร','วารสารนานาชาติที่อยู่ในข้อมูลสากร'),
				(u'ผลงานวิชาการอื่นๆ','ผลงานวิชาการอื่นๆ'),
				),
			label = "ระดับ",
			widget = forms.RadioSelect,
			initial = u'นานาชาติมี impact factor',
			required = False,
		)

	degree2 = forms.ChoiceField(
			choices = ( 
				(u'สิ่งประดิษฐ์ได้รับการจดสิทธิบัตร','สิ่งประดิษฐ์ได้รับการจดสิทธิบัตร'),
				(u'สิทธิบัตรที่ถูกนำไปใช้ประโยชน์','สิทธิบัตรที่ถูกนำไปใช้ประโยชน์'),
				),
			label = "สิงประเดิษฐ์",
			widget = forms.RadioSelect,
			required = False,
		)

	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(ResearchForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.layout = Layout(

				Field('research_name'),
				Field('assist_name'),
				Field('journal_name'),
				Field('year'),
				Field('ratio',),
				Field('degree',),
				Field('degree2',),
				Field('comment',),
				Div(
					Submit('submit','Submit'),
					style='text-align:center;'
					)
		)

	class Meta:
		model = Research
		fields = [
						"research_name",
						"assist_name",
						"journal_name",
						"year",
						"ratio",
						"degree",
						"degree2",
						"comment",
			]		
		