from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Custom User model for SmartPath Academy"""
    
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('INSTRUCTOR', 'Instructor'),
        ('ADMIN', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT',
        help_text='User role in the platform'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text='User profile picture'
    )
    bio = models.TextField(blank=True, help_text='Short biography')
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Fix the reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class StudentProfile(models.Model):
    """Extended profile for student users"""
    
    LEARNING_STYLE_CHOICES = [
        ('VISUAL', 'Visual'),
        ('AUDITORY', 'Auditory'),
        ('KINESTHETIC', 'Kinesthetic'),
        ('READING_WRITING', 'Reading/Writing'),
    ]
    
    PACE_CHOICES = [
        ('SLOW', 'Slow'),
        ('MEDIUM', 'Medium'),
        ('FAST', 'Fast'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    learning_style = models.CharField(
        max_length=20,
        choices=LEARNING_STYLE_CHOICES,
        default='VISUAL',
        help_text='Preferred learning style'
    )
    current_level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Current level (1-10)'
    )
    points = models.PositiveIntegerField(
        default=0,
        help_text='Total points earned'
    )
    total_xp = models.PositiveIntegerField(
        default=0,
        help_text='Total experience points'
    )
    streak_days = models.PositiveIntegerField(
        default=0,
        help_text='Consecutive days of activity'
    )
    last_activity_date = models.DateField(
        blank=True,
        null=True,
        help_text='Last date of activity'
    )
    preferred_pace = models.CharField(
        max_length=10,
        choices=PACE_CHOICES,
        default='MEDIUM',
        help_text='Preferred learning pace'
    )
    strengths = models.JSONField(
        default=list,
        help_text='List of student strengths'
    )
    weaknesses = models.JSONField(
        default=list,
        help_text='List of areas to improve'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Student Profile - Level {self.current_level}"
