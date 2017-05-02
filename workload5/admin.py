from django.contrib import admin

from .models import Support
# Register your models here.
class SupportModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"support_list",
					"degree",
					"kind",
					"committee",
					"comment",
					"date",
					]
	class meta:
		model = Support

admin.site.register(Support, SupportModelAdmin)