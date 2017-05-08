from django.contrib import admin

from .models import Benefit
# Register your models here.
class BenefitModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"benefit_list",
					"benefit_name",
					"person_name",
					"date",
					]
	class meta:
		model = Benefit

admin.site.register(Benefit, BenefitModelAdmin)