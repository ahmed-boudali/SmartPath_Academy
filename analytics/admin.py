from django.contrib import admin
from .models import UserActivity, QuizAttempt


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'related_object_type', 'timestamp', 'duration']
    list_filter = ['activity_type', 'timestamp', 'related_object_type']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'percentage', 'time_taken', 'started_at', 'completed_at']
    list_filter = ['started_at', 'completed_at', 'quiz']
    search_fields = ['student__username', 'student__email', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at']
    date_hierarchy = 'started_at'
