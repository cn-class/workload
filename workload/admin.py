
from django.contrib import admin

from .models import Teaching,Program
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
					"comment",
					"date",
					]
	class meta:
		model = Teaching


class ProgramModelAdmin(admin.ModelAdmin):
	list_display = [
					"name",
					
					]
	class meta:
		model = Program


admin.site.register(Teaching, TeachingModelAdmin)
admin.site.register(Program, ProgramModelAdmin)