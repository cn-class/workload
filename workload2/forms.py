#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row,Field
from crispy_forms.bootstrap import AppendedText,PrependedText,FormActions,InlineField,StrictButton

from .models import Thesis

class ThesisForm(forms.ModelForm):

	user = forms.ModelChoiceField(
	        queryset=Thesis.objects.all(),
	        widget=forms.HiddenInput(),
	        required = False,
        )

	thesis_name = forms.CharField(
			label = "ชื่อโครงงาน/วิทยานิพนธ์",
			required = True,
		)

	ratio = forms.IntegerField(
			label = "สัดส่วนการสอน(คิดเป็นร้อยละ)",
			required = True,
		)

	degree = forms.ChoiceField(
			choices = ( 
				(u'โครงงาน','โครงงาน'),
				(u'สาระนิพนธ์','สาระนิพนธ์'),
				(u'วิทยานิพนธ์ ป.โทร','วิทยานิพนธ์ ป.โทร'),
				(u'วิทยานิพนธ์ ป. เอก','วิทยานิพนธ์ ป. เอก'),
				),
			label = "ระดับ",
			widget = forms.RadioSelect,
			initial = u'โครงงาน',
			required = True,
		)

	program_ID = forms.ChoiceField(
			choices = ( 
				(u'โครงการปกติ','โครงการปกติ'),
				(u'โครงการพิเศษได้ค่าตอบแทน','โครงการพิเศษได้ค่าตอบแทน'),
				(u'โครงการพิเศษไม่ได้ค่าตอบแทน','โครงการพิเศษไม่ได้ค่าตอบแทน'),
				(u'งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน','งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน'),
				),
			label = "ประเภทโครงการ",
			widget = forms.RadioSelect,
			initial = u'โครงการปกติ',
			required = True,
		)

	comment = forms.CharField(
			label = "หมายเหตุ",
			widget = forms.Textarea(),
			required = False,
		)

	def __init__(self, *args, **kwargs):

		super(ThesisForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 col-md-offset-1'
		self.helper.field_class = 'col-md-5'
		self.helper.layout = Layout(

				Field('thesis_name'),
				Field('ratio',),
				Field('degree',),
				Field('program_ID',),
				Field('comment',),
				Div(
					Submit('submit','Submit'),
					style='text-align:center;'
					)
		)

	class Meta:
		model = Thesis
		fields = [
						"thesis_name",
						"ratio",
						"degree",
						"program_ID",
						"comment",
			]		
		