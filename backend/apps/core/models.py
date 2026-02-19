from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'languages'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    COUNTRY_CHOICES = [
        ('CH', 'Switzerland'),
        ('DE', 'Germany'),
        ('AT', 'Austria'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    native_language = models.CharField(max_length=10, default='es')
    target_country = models.CharField(max_length=5, choices=COUNTRY_CHOICES, default='CH')
    daily_goal_minutes = models.IntegerField(default=10)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='Europe/Zurich')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username} ({self.target_country})"


class UserLanguage(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Mastery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_languages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    current_level = models.CharField(max_length=5, choices=LEVEL_CHOICES, default='A1')
    xp_points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_languages'
        unique_together = ['user', 'language']

    def __str__(self):
        return f"{self.user.username} - {self.language.name} ({self.current_level})"
