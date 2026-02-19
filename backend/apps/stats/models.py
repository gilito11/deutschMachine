from django.db import models
from django.contrib.auth.models import User


class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_activities')
    activity_date = models.DateField()
    minutes_practiced = models.IntegerField(default=0)
    cards_reviewed = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    conversations_count = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)

    class Meta:
        db_table = 'daily_activity'
        unique_together = ['user', 'activity_date']
        ordering = ['-activity_date']

    def __str__(self):
        return f"{self.user.username} - {self.activity_date} ({self.xp_earned} XP)"
