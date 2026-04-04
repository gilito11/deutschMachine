from django.contrib import admin
from .models import ConversationSession, Message


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario', 'language', 'user_level', 'message_count', 'created_at']
    list_filter = ['scenario', 'language', 'user_level']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'created_at']
    list_filter = ['role']

    def content_preview(self, obj):
        return obj.content[:80]
