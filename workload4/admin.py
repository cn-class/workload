from django.contrib import admin

from .models import Document
# Register your models here.
class DocumentModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"subject_ID",
					"subject_name",
					"assist_name",
					"page",
					"ratio",
					"degree",
					"comment"
					]
	class meta:
		model = Document

admin.site.register(Document, DocumentModelAdmin)