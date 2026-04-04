from django.db import models
from django.contrib.auth.models import User
from core.models import Language


class ConversationSession(models.Model):
    SCENARIO_CHOICES = [
        ('free', 'Free Conversation'),
        ('job_interview', 'Job Interview'),
        ('supermarket', 'At the Supermarket'),
        ('apartment', 'Apartment Hunting'),
        ('restaurant', 'At the Restaurant'),
        ('doctor', 'Doctor Visit'),
        ('friends', 'Meeting Friends'),
        ('transport', 'Public Transport'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    scenario = models.CharField(max_length=30, choices=SCENARIO_CHOICES, default='free')
    title = models.CharField(max_length=200, blank=True)
    user_level = models.CharField(max_length=5, default='A1')
    message_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversation_sessions'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_scenario_display()} ({self.created_at})"


class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    session = models.ForeignKey(ConversationSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    correction = models.TextField(blank=True, help_text='Grammar correction if user made errors')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversation_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:60]}"
