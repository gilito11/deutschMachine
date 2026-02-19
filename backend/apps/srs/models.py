from datetime import date
from django.db import models
from django.contrib.auth.models import User
from vocabulary.models import VocabularyItem


class SRSCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='srs_cards')
    vocabulary_item = models.ForeignKey(VocabularyItem, on_delete=models.CASCADE, related_name='srs_cards')
    easiness_factor = models.FloatField(default=2.5)
    interval_days = models.IntegerField(default=0)
    repetitions = models.IntegerField(default=0)
    next_review_date = models.DateField(default=date.today)
    last_review_date = models.DateField(null=True, blank=True)
    last_quality = models.IntegerField(null=True, blank=True)
    total_reviews = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'srs_cards'
        unique_together = ['user', 'vocabulary_item']

    def __str__(self):
        return f"{self.user.username}: {self.vocabulary_item.word} (next: {self.next_review_date})"

    @property
    def is_due(self):
        return self.next_review_date <= date.today()

    @property
    def accuracy(self):
        if self.total_reviews == 0:
            return 0
        return round(self.correct_count / self.total_reviews * 100)


class ReviewLog(models.Model):
    REVIEW_TYPE_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('practice', 'Practice'),
        ('cram', 'Cram'),
    ]

    srs_card = models.ForeignKey(SRSCard, on_delete=models.CASCADE, related_name='review_logs')
    quality = models.IntegerField()
    response_time_ms = models.IntegerField(null=True, blank=True)
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPE_CHOICES, default='scheduled')
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_logs'
        ordering = ['-reviewed_at']
