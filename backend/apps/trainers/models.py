from django.db import models
from django.contrib.auth.models import User


class GenderDrillScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gender_scores')
    total_attempts = models.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gender_drill_scores'

    def __str__(self):
        return f"{self.user.username} - {self.accuracy}%"

    @property
    def accuracy(self):
        if self.total_attempts == 0:
            return 0
        return round(self.correct_attempts / self.total_attempts * 100)


class CaseDrillScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_scores')
    total_attempts = models.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'case_drill_scores'

    def __str__(self):
        return f"{self.user.username} - {self.accuracy}%"

    @property
    def accuracy(self):
        if self.total_attempts == 0:
            return 0
        return round(self.correct_attempts / self.total_attempts * 100)
