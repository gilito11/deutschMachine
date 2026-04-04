from django.contrib import admin
from .models import GenderDrillScore, CaseDrillScore


@admin.register(GenderDrillScore)
class GenderDrillScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_attempts', 'correct_attempts', 'accuracy', 'best_streak']


@admin.register(CaseDrillScore)
class CaseDrillScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_attempts', 'correct_attempts', 'accuracy', 'best_streak']
