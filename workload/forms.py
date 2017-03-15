#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions

from .models import Teaching

class TeachingForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Teaching.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	subject_ID = forms.CharField(
			label = "รหัสวิชา",
			required = True,
		)

	subject = forms.CharField(
			label = "ชื่อวิชา",
			required = True,
		)

	ratio = forms.IntegerField(
			label = "สัดส่วนการสอน(คิดเป็นร้อยละ)",
			required = True,
		)

	num_of_lecture = forms.IntegerField(
			label = "จำนวนหน่วยกิตการบรรยาย",
			required = True,
		)

	num_of_lab = forms.IntegerField(
			label = "จำนวนหน่วยกิตการปฏิบัติการ",
			required = True,
		)

	program_ID = forms.ChoiceField(
			choices = ( 
				('โครงการปกติ','โครงการปกติ'),
				('โครงการพิเศษได้ค่าตอบแทน','โครงการพิเศษได้ค่าตอบแทน'),
				('โครงการพิเศษไม่ได้ค่าตอบแทน','โครงการพิเศษไม่ได้ค่าตอบแทน'),
				('งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน','งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน'),
				),
			label = "ประเภทโครงการ",
			widget = forms.RadioSelect,
			initial = 'option_one',
			required = True,
		)

	num_of_student = forms.IntegerField(
			label = "จำนวนนักศึกษา",
			required = True,
		)

	ratio_of_score = forms.CharField(
			label = "อัตราส่วนที่ใช้ในการคำนวณคะแนน",
			required = True,
		)

	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.layout = Layout(

			Field('subject_ID'),
			Field('subject', css_class='input-xlarge', style='width: 300px;'),
			Field('ratio',),
			Field('num_of_lecture',),
			Field('num_of_lab',),
			Field('program_ID',),
			Field('num_of_student',),
			Field('ratio_of_score',),
			Field('comment',),

		)

	class Meta:
			model = Teaching
			fields = [
					"subject_ID",
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
	