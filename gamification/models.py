from django.db import models
from django.conf import settings


class Badge(models.Model):
    """Achievement badges for students"""
    
    BADGE_TYPE_CHOICES = [
        ('ACHIEVEMENT', 'Achievement'),
        ('MILESTONE', 'Milestone'),
        ('SPECIAL', 'Special'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(
        max_length=100,
        help_text='Icon class or image name'
    )
    badge_type = models.CharField(
        max_length=20,
        choices=BADGE_TYPE_CHOICES,
        help_text='Type of badge'
    )
    requirement = models.JSONField(
        help_text='JSON containing conditions to earn this badge'
    )
    points_reward = models.PositiveIntegerField(
        default=0,
        help_text='Points awarded when badge is earned'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_badge_type_display()})"


class UserBadge(models.Model):
    """Badges earned by users"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='earned_badges'
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name='earned_by'
    )
    earned_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(
        default=True,
        help_text='Whether to display this badge on profile'
    )

    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
        verbose_name = 'User Badge'
        verbose_name_plural = 'User Badges'

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"


class Level(models.Model):
    """User progression levels"""
    level_number = models.PositiveIntegerField(
        unique=True,
        help_text='Level number (1, 2, 3, etc.)'
    )
    name = models.CharField(
        max_length=50,
        help_text='Level name (e.g., Beginner, Novice, etc.)'
    )
    xp_required = models.PositiveIntegerField(
        help_text='Total XP required to reach this level'
    )
    icon = models.CharField(
        max_length=100,
        help_text='Icon class or image name'
    )
    color = models.CharField(
        max_length=50,
        help_text='Color code for level badge'
    )
    rewards = models.JSONField(
        default=dict,
        help_text='JSON containing rewards for reaching this level'
    )

    class Meta:
        ordering = ['level_number']

    def __str__(self):
        return f"Level {self.level_number}: {self.name} ({self.xp_required} XP)"


class Achievement(models.Model):
    """User achievements and milestones"""
    
    ACHIEVEMENT_TYPE_CHOICES = [
        ('COURSE_COMPLETION', 'Course Completion'),
        ('STREAK', 'Streak'),
        ('QUIZ_MASTER', 'Quiz Master'),
        ('SPEED_LEARNER', 'Speed Learner'),
        ('ENGAGEMENT', 'Engagement'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(
        max_length=30,
        choices=ACHIEVEMENT_TYPE_CHOICES,
        help_text='Type of achievement'
    )
    achieved_at = models.DateTimeField(auto_now_add=True)
    points_earned = models.PositiveIntegerField(
        default=0,
        help_text='Points earned for this achievement'
    )

    class Meta:
        ordering = ['-achieved_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Leaderboard(models.Model):
    """Leaderboard rankings for different time periods"""
    
    PERIOD_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('ALL_TIME', 'All Time'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries'
    )
    period = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        help_text='Leaderboard time period'
    )
    rank = models.PositiveIntegerField(help_text='User rank in this period')
    total_points = models.PositiveIntegerField(
        default=0,
        help_text='Total points in this period'
    )
    total_xp = models.PositiveIntegerField(
        default=0,
        help_text='Total XP in this period'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'period']
        ordering = ['period', 'rank']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.get_period_display()})"
