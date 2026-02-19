from django.contrib import admin
from .models import Lesson, Exercise, UserLessonProgress


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'difficulty_level', 'lesson_type', 'sort_order', 'is_active']
    list_filter = ['language', 'difficulty_level', 'lesson_type']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExerciseInline]


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'correct_answers', 'total_answered', 'xp_earned']
    list_filter = ['is_completed']
