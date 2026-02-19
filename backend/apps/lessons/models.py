import json
from django.db import models
from django.contrib.auth.models import User
from core.models import Language
from vocabulary.models import Topic


class Lesson(models.Model):
    LESSON_TYPES = [
        ('vocabulary', 'Vocabulary'),
        ('grammar', 'Grammar'),
        ('dialogue', 'Dialogue'),
        ('scenario', 'Scenario'),
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='lessons')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='vocabulary')
    difficulty_level = models.CharField(max_length=5, default='A1')
    sort_order = models.IntegerField(default=0)
    icon = models.CharField(max_length=10, blank=True)
    xp_reward = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lessons'
        ordering = ['difficulty_level', 'sort_order']

    def __str__(self):
        return f"{self.title} ({self.language.code} {self.difficulty_level})"

    def exercise_count(self):
        return self.exercises.count()


class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('fill_blank', 'Fill in the Blank'),
        ('translation', 'Translation'),
        ('matching', 'Matching'),
        ('reorder', 'Reorder Words'),
        ('listening', 'Listening'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    sort_order = models.IntegerField(default=0)
    question = models.TextField()
    correct_answer = models.CharField(max_length=500)
    options = models.JSONField(default=list, blank=True, help_text='List of options for multiple_choice/matching')
    hint = models.CharField(max_length=500, blank=True)
    explanation = models.TextField(blank=True)
    xp_value = models.IntegerField(default=2)

    class Meta:
        db_table = 'exercises'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.get_exercise_type_display()}: {self.question[:60]}"

    def get_shuffled_options(self):
        import random
        opts = list(self.options) if self.options else []
        if self.exercise_type == 'multiple_choice' and self.correct_answer not in opts:
            opts.append(self.correct_answer)
        random.shuffle(opts)
        return opts


class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    current_exercise = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    total_answered = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    xp_earned = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_lesson_progress'
        unique_together = ['user', 'lesson']

    def __str__(self):
        status = 'Done' if self.is_completed else f'{self.current_exercise}/{self.lesson.exercise_count()}'
        return f"{self.user.username} - {self.lesson.title} ({status})"

    @property
    def accuracy(self):
        if self.total_answered == 0:
            return 0
        return round(self.correct_answers / self.total_answered * 100)

    @property
    def progress_pct(self):
        total = self.lesson.exercise_count()
        if total == 0:
            return 0
        return round(self.current_exercise / total * 100)
