from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum
from courses.models import Enrollment, LessonProgress
from gamification.models import Achievement, UserBadge
from analytics.models import UserActivity
from datetime import datetime, timedelta
import json


@login_required
def student_dashboard(request):
    """Student dashboard view"""
    user = request.user
    
    try:
        student_profile = user.studentprofile
    except:
        student_profile = None

    # Get statistics
    enrolled_courses = Enrollment.objects.filter(student=user).count()
    lessons_completed = LessonProgress.objects.filter(
        student=user,
        status='COMPLETED'
    ).count()
    
    # Calculate stats
    stats = {
        'enrolled_courses': enrolled_courses,
        'lessons_completed': lessons_completed,
        'new_enrollments': Enrollment.objects.filter(
            student=user,
            enrolled_at__gte=datetime.now() - timedelta(days=30)
        ).count(),
        'recent_completions': LessonProgress.objects.filter(
            student=user,
            status='COMPLETED',
            completed_at__gte=datetime.now() - timedelta(days=7)
        ).count(),
        'xp_earned_today': 0,  # Implement based on your XP system
        'avg_quiz_score': 75,  # Calculate from QuizAttempt model
        'completion_rate': 65,  # Calculate based on enrollments
        'study_time_hours': 12,  # Calculate from activity data
        'badges_count': UserBadge.objects.filter(user=user).count(),
    }

    # Get continue learning courses
    continue_learning = Enrollment.objects.filter(
        student=user,
        completed_at__isnull=True
    ).select_related('course', 'course__instructor').order_by('-enrolled_at')[:3]

    # Get recent achievements
    recent_achievements = Achievement.objects.filter(
        user=user
    ).order_by('-achieved_at')[:5]

    # Prepare progress data for chart (last 7 days)
    progress_data = []
    progress_labels = []
    for i in range(6, -1, -1):
        date = datetime.now().date() - timedelta(days=i)
        count = LessonProgress.objects.filter(
            student=user,
            completed_at__date=date,
            status='COMPLETED'
        ).count()
        progress_data.append(count)
        progress_labels.append(date.strftime('%a'))

    context = {
        'student_profile': student_profile,
        'stats': stats,
        'continue_learning': continue_learning,
        'recent_achievements': recent_achievements,
        'progress_data': json.dumps(progress_data),
        'progress_labels': json.dumps(progress_labels),
        'title': 'Dashboard',
    }

    return render(request, 'dashboard/student_dashboard.html', context)


def course_list(request):
    """Browse courses view"""
    from courses.models import Course, Category
    
    # Get all published courses
    courses = Course.objects.filter(is_published=True).select_related(
        'category', 'instructor'
    ).order_by('-created_at')

    # Get categories with course count
    categories = Category.objects.annotate(
        course_count=Count('courses')
    ).order_by('name')

    context = {
        'courses': courses,
        'categories': categories,
        'title': 'Browse Courses',
        'subTitle': 'All Courses',
    }

    return render(request, 'courses/course_list.html', context)


def api_root(request):
    """API root endpoint - redirect to dashboard for logged in users"""
    if request.user.is_authenticated:
        return redirect('student-dashboard')
    return redirect('login')
