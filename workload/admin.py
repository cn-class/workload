
from django.contrib import admin

from .models import Teaching
# Register your models here.
class TeachingModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"subject_ID",
					"subject",
					"ratio",
					"num_of_lecture",
					"num_of_lab",
					"program_ID",
					"num_of_student",
					"ratio_of_score",
					"comment",
					"date"
					]
	class meta:
		model = Teaching

admin.site.register(Teaching, TeachingModelAdmin)