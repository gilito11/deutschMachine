from django.db import models
from core.models import Language


class Topic(models.Model):
    CATEGORY_CHOICES = [
        ('daily_life', 'Daily Life'),
        ('work', 'Work'),
        ('social', 'Social'),
        ('travel', 'Travel'),
        ('culture', 'Culture'),
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=5, default='A1')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    country_context = models.CharField(max_length=5, blank=True, help_text='CH, DE, or blank for both')
    sort_order = models.IntegerField(default=0)
    icon = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'topics'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class VocabularyItem(models.Model):
    POS_CHOICES = [
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adj', 'Adjective'),
        ('adv', 'Adverb'),
        ('phrase', 'Phrase'),
        ('prep', 'Preposition'),
        ('conj', 'Conjunction'),
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='vocabulary')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='vocabulary_items')
    word = models.CharField(max_length=255)
    translation_es = models.CharField(max_length=255)
    pronunciation_ipa = models.CharField(max_length=255, blank=True)
    part_of_speech = models.CharField(max_length=20, choices=POS_CHOICES)
    gender = models.CharField(max_length=10, blank=True, help_text='der/die/das for German')
    plural = models.CharField(max_length=255, blank=True)
    example_sentence = models.TextField(blank=True)
    example_translation = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=5, default='A1')
    region_variant = models.CharField(max_length=5, blank=True, help_text='CH or DE for regional')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vocabulary_items'
        ordering = ['word']

    def __str__(self):
        prefix = f"{self.gender} " if self.gender else ""
        return f"{prefix}{self.word} → {self.translation_es}"
