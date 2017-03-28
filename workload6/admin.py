from django.contrib import admin

from .models import Position
# Register your models here.
class PositionModelAdmin(admin.ModelAdmin):
	list_display = [
					"user",
					"position_name",
					"time_start",
					"time_end",
					"comment"
					]
	class meta:
		model = Position

admin.site.register(Position, PositionModelAdmin)