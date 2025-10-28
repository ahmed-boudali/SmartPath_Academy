from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ['sender', 'message_text', 'timestamp', 'helpful_rating']
    readonly_fields = ['timestamp']
    can_delete = False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'message_count', 'is_active', 'started_at', 'last_message_at']
    list_filter = ['is_active', 'started_at', 'last_message_at']
    search_fields = ['student__username', 'student__email', 'title']
    readonly_fields = ['started_at', 'last_message_at']
    inlines = [ChatMessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'message_preview', 'timestamp', 'helpful_rating']
    list_filter = ['sender', 'timestamp', 'helpful_rating']
    search_fields = ['message_text', 'session__student__username']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    message_preview.short_description = 'Message'
