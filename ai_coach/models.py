from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class ChatSession(models.Model):
    """Chat sessions between students and AI coach"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    title = models.CharField(
        max_length=200,
        default='New Conversation',
        help_text='Session title'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp of last message in this session'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this session is still active'
    )

    class Meta:
        ordering = ['-last_message_at']
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'

    def __str__(self):
        return f"{self.student.username} - {self.title}"


class ChatMessage(models.Model):
    """Individual messages in chat sessions"""
    
    SENDER_CHOICES = [
        ('USER', 'User'),
        ('AI', 'AI'),
    ]
    
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES,
        help_text='Who sent this message'
    )
    message_text = models.TextField(help_text='Message content')
    timestamp = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(
        blank=True,
        null=True,
        help_text='Additional context or metadata for the message'
    )
    helpful_rating = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='User rating of AI response (1-5)'
    )

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        preview = self.message_text[:50] + '...' if len(self.message_text) > 50 else self.message_text
        return f"{self.get_sender_display()}: {preview}"
