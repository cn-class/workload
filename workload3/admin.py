from django.contrib import admin

from .models import Research
# Register your models here.
class ResearchModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"research_name",
					"assist_name",
					"journal_name",
					"year",
					"ratio",
					"degree",
					"degree2",
					"comment",
					"date",
					]
	class meta:
		model = Research

admin.site.register(Research, ResearchModelAdmin)