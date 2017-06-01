#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton,FieldWithButtons

from django.utils.timezone import datetime

from .models import Teaching,Program

class TeachingForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Teaching.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	# date = forms.DateField(
	# 		label = "วันที่",
	# 		widget=forms.SelectDateWidget,
	# 		initial = datetime.date.today,
	# 		required = False,

	# 	)

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

	program_ID = forms.ModelChoiceField(
	        queryset=Program.objects.all(),
	        required = True,
	        label = "ประเภทโครงการ",
			widget = forms.RadioSelect,

        )

	# program_ID = forms.ChoiceField(
	# 		choices = ( 
	# 			(u'โครงการปกติ','โครงการปกติ'),
	# 			(u'โครงการพิเศษได้ค่าตอบแทน','โครงการพิเศษได้ค่าตอบแทน'),
	# 			(u'โครงการพิเศษไม่ได้ค่าตอบแทน','โครงการพิเศษไม่ได้ค่าตอบแทน'),
	# 			(u'งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน','งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน'),
	# 			),
	# 		label = "ประเภทโครงการ",
	# 		widget = forms.RadioSelect,
	# 		initial = u'โครงการปกติ',
	# 		required = True,
	# 	)

	num_of_student = forms.IntegerField(
			label = "จำนวนนักศึกษา",
			required = True,
		)

	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(TeachingForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.form_id = 'teaching_sub'
		# self.fields['program_ID'].queryset = Program.objects.all()
		self.helper.layout = Layout(

				Field('subject_ID'),
				Field('subject'),
				Field('ratio',),
				Field('num_of_lecture',),
				Field('num_of_lab',),
				Field('program_ID',),
				Field('num_of_student',),
				Field('comment',),
				FormActions(
					Submit('submit','Submit'),
					Button('cancel','Cancel' ,css_class='btn-default')
					
					)
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
		model = Teaching
		fields = [
					"year",
				]