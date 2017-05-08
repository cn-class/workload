#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from django.utils.timezone import datetime

from .models import Benefit

class BenefitForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Benefit.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	benefit_list = forms.ChoiceField(
			choices = ( 
				(u'อาจารย์ได้รับรางวัลทางวิชาการหรือวิชาชีพระดับหน่วยงานภายนอกมหาวิทยาลัย',
					'อาจารย์ได้รับรางวัลทางวิชาการหรือวิชาชีพระดับหน่วยงานภายนอกมหาวิทยาลัย'),
				(u'อาจารย์ได้รับรางวัลทางวิชาการหรือวิชาชีพระดับชาติ/นานาชาติ',
					'อาจารย์ได้รับรางวัลทางวิชาการหรือวิชาชีพระดับชาติ/นานาชาติ'),
				(u'อาจารย์ที่ปรึกษากิจกรรมการแข่งขันทางวิชาการของนักศึกษาที่ได้รับรางวัลระดับหน่วยงาน',
					'อาจารย์ที่ปรึกษากิจกรรมการแข่งขันทางวิชาการของนักศึกษาที่ได้รับรางวัลระดับหน่วยงาน'),
				(u'อาจารย์ที่ปรึกษากิจกรรมการแข่งขันทางวิชาการของนักศึกษาที่ได้รับรางวัลระดับชาติ/นานาชาติ',
					'อาจารย์ที่ปรึกษากิจกรรมการแข่งขันทางวิชาการของนักศึกษาที่ได้รับรางวัลระดับชาติ/นานาชาติ'),
				(u'อาจารย์ที่ให้ความร่วมมือในการจัดประชุมวิชาการของคณะ',
					'อาจารย์ที่ให้ความร่วมมือในการจัดประชุมวิชาการของคณะ'),
				),
			label = "รายการ",
			widget = forms.RadioSelect,
			initial = u'อาจารย์ได้รับรางวัลทางวิชาการหรือวิชาชีพระดับหน่วยงานภายนอกมหาวิทยาลัย',
			required = True,
		)

	benefit_name = forms.CharField(
			label = "ชื่อผลงาน",
			required = True,
		)

	person_name = forms.CharField(
			label = "ชื่อผู้เข้าร่วมการแข่งขัน",
			required = True,
		)

	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(BenefitForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.layout = Layout(

				Field('benefit_list'),
				Field('benefit_name',),
				Field('person_name'),
				Field('comment',),
				Div(
					Submit('submit','Submit'),
					style='text-align:center;'
					)
		)

	class Meta:
		model = Benefit
		fields = [
						"benefit_list",
						"benefit_name",
						"person_name",
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
		model = Benefit
		fields = [
					"year",
				]