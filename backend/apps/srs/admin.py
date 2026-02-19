from django.contrib import admin
from .models import SRSCard, ReviewLog


@admin.register(SRSCard)
class SRSCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'vocabulary_item', 'next_review_date', 'repetitions', 'easiness_factor']
    list_filter = ['user', 'next_review_date']


@admin.register(ReviewLog)
class ReviewLogAdmin(admin.ModelAdmin):
    list_display = ['srs_card', 'quality', 'response_time_ms', 'reviewed_at']
