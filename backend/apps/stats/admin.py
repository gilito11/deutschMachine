from django.contrib import admin
from .models import DailyActivity


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_date', 'cards_reviewed', 'xp_earned']
    list_filter = ['user', 'activity_date']
