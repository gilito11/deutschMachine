from django.contrib import admin
from .models import Language, UserProfile, UserLanguage


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'target_country', 'current_streak', 'daily_goal_minutes']


@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'current_level', 'xp_points', 'is_active']
