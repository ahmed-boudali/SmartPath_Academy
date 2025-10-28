from django.db import models
from django.conf import settings
from courses.models import Quiz


class UserActivity(models.Model):
    """Track all user activities in the platform"""
    
    ACTIVITY_TYPE_CHOICES = [
        ('LOGIN', 'Login'),
        ('LESSON_VIEW', 'Lesson View'),
        ('LESSON_COMPLETE', 'Lesson Complete'),
        ('QUIZ_START', 'Quiz Start'),
        ('QUIZ_COMPLETE', 'Quiz Complete'),
        ('CHAT', 'Chat'),
        ('ENROLLMENT', 'Enrollment'),
        ('BADGE_EARNED', 'Badge Earned'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        help_text='Type of activity'
    )
    related_object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='ID of the related object (course, lesson, etc.)'
    )
    related_object_type = models.CharField(
        max_length=50,
        blank=True,
        help_text='Type of the related object'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Duration in seconds'
    )
    metadata = models.JSONField(
        default=dict,
        help_text='Additional metadata about the activity'
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User Activities'
        indexes = [
            models.Index(fields=['user', 'activity_type', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class QuizAttempt(models.Model):
    """Track quiz attempts and results"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the quiz was completed'
    )
    score = models.PositiveIntegerField(
        default=0,
        help_text='Total points scored'
    )
    percentage = models.FloatField(
        default=0.0,
        help_text='Score as percentage (0-100)'
    )
    time_taken = models.PositiveIntegerField(
        default=0,
        help_text='Time taken in seconds'
    )
    answers = models.JSONField(
        default=dict,
        help_text='JSON containing all answers submitted'
    )

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.percentage:.1f}%)"
