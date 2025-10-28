from django.contrib import admin
from .models import Category, Course, Lesson, Quiz, Question, Answer, Enrollment, LessonProgress


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'content_type', 'duration', 'is_free']
    ordering = ['order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'difficulty_level', 'is_published', 'created_at']
    list_filter = ['difficulty_level', 'is_published', 'category', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'cover_image')
        }),
        ('Course Details', {
            'fields': ('category', 'instructor', 'difficulty_level', 'estimated_duration')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'content_type', 'duration', 'is_free']
    list_filter = ['content_type', 'is_free', 'course']
    search_fields = ['title', 'content', 'course__title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'order', 'points']
    ordering = ['order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'passing_score', 'time_limit', 'created_at']
    list_filter = ['passing_score', 'created_at']
    search_fields = ['title', 'lesson__title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    fields = ['answer_text', 'is_correct', 'order']
    ordering = ['order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'quiz', 'question_type', 'order', 'points']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text', 'quiz__title']
    inlines = [AnswerInline]
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text_short', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['answer_text', 'question__question_text']
    
    def answer_text_short(self, obj):
        return obj.answer_text[:50] + '...' if len(obj.answer_text) > 50 else obj.answer_text
    answer_text_short.short_description = 'Answer'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'enrolled_at', 'completed_at']
    list_filter = ['enrolled_at', 'completed_at', 'course']
    search_fields = ['student__username', 'student__email', 'course__title']
    readonly_fields = ['enrolled_at']
    
    fieldsets = (
        ('Enrollment Info', {
            'fields': ('student', 'course', 'enrolled_at')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'current_lesson', 'completed_at')
        }),
    )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'status', 'time_spent', 'score', 'completed_at']
    list_filter = ['status', 'completed_at', 'lesson__course']
    search_fields = ['student__username', 'lesson__title']
    readonly_fields = ['created_at', 'updated_at']
