from django.contrib import admin

from .models import Thesis
# Register your models here.
class ThesisModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"thesis_name",
					"student_name",
					"ratio",
					"degree",
					"program_ID",
					"comment",
					"date",
					"count",
					]
	class meta:
		model = Thesis

admin.site.register(Thesis, ThesisModelAdmin)