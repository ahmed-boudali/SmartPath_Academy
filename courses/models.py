from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Course categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    """Main course model"""
    
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = models.ImageField(
        upload_to='course_covers/',
        blank=True,
        null=True,
        help_text='Course cover image'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_courses'
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        help_text='Course difficulty level'
    )
    estimated_duration = models.PositiveIntegerField(
        help_text='Duration in hours'
    )
    is_published = models.BooleanField(
        default=False,
        help_text='Whether the course is published and visible to students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_level_display()})"


class Lesson(models.Model):
    """Individual lessons within courses"""
    
    CONTENT_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
        ('INTERACTIVE', 'Interactive'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0, help_text='Lesson order in the course')
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        help_text='Type of lesson content'
    )
    content = models.TextField(help_text='Lesson content or description')
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text='YouTube or video URL'
    )
    duration = models.PositiveIntegerField(
        help_text='Duration in minutes'
    )
    is_free = models.BooleanField(
        default=False,
        help_text='Whether this lesson is available for free preview'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}: {self.title}"


class Quiz(models.Model):
    """Quizzes associated with lessons"""
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='quiz'
    )
    title = models.CharField(max_length=200)
    passing_score = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Passing score percentage (0-100)'
    )
    time_limit = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Time limit in minutes (optional)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f"Quiz: {self.title}"


class Question(models.Model):
    """Quiz questions"""
    
    QUESTION_TYPE_CHOICES = [
        ('MULTIPLE_CHOICE', 'Multiple Choice'),
        ('TRUE_FALSE', 'True/False'),
        ('SHORT_ANSWER', 'Short Answer'),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text='Question order in quiz')
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        help_text='Type of question'
    )
    points = models.PositiveIntegerField(
        default=10,
        help_text='Points awarded for correct answer'
    )
    explanation = models.TextField(
        blank=True,
        help_text='Explanation shown after answering'
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"


class Answer(models.Model):
    """Possible answers for quiz questions"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(
        default=False,
        help_text='Whether this is the correct answer'
    )
    order = models.PositiveIntegerField(default=0, help_text='Answer order')

    class Meta:
        ordering = ['order']

    def __str__(self):
        status = '✓' if self.is_correct else '✗'
        return f"{status} {self.answer_text[:50]}"


class Enrollment(models.Model):
    """Track student enrollments in courses"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the student completed the course'
    )
    progress_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Course completion percentage (0-100)'
    )
    current_lesson = models.ForeignKey(
        Lesson,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='current_students',
        help_text='The lesson the student is currently on'
    )

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title} ({self.progress_percentage}%)"


class LessonProgress(models.Model):
    """Track individual lesson completion"""
    
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NOT_STARTED',
        help_text='Current status of the lesson'
    )
    time_spent = models.PositiveIntegerField(
        default=0,
        help_text='Time spent in minutes'
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the lesson was completed'
    )
    score = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Quiz score if applicable (0-100)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'lesson']
        verbose_name_plural = 'Lesson Progress'

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title} ({self.get_status_display()})"
