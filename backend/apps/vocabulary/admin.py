from django.contrib import admin
from .models import Topic, VocabularyItem


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'category', 'difficulty_level', 'country_context', 'is_active']
    list_filter = ['language', 'category', 'difficulty_level']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VocabularyItem)
class VocabularyItemAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation_es', 'language', 'topic', 'part_of_speech', 'difficulty_level']
    list_filter = ['language', 'topic', 'part_of_speech', 'difficulty_level']
    search_fields = ['word', 'translation_es']
