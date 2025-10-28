"""
Placeholder views for frontend pages
These return simple pages until full implementation
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def my_courses(request):
    """My enrolled courses page"""
    context = {'title': 'My Courses', 'subTitle': 'Enrolled Courses'}
    return render(request, 'placeholder.html', context)


@login_required
def ai_chat(request):
    """AI Coach chat interface"""
    context = {'title': 'AI Coach', 'subTitle': 'Chat with AI'}
    return render(request, 'placeholder.html', context)


@login_required
def student_progress(request):
    """Student progress and analytics"""
    context = {'title': 'My Progress', 'subTitle': 'Analytics'}
    return render(request, 'placeholder.html', context)


@login_required
def leaderboard(request):
    """Leaderboard rankings"""
    context = {'title': 'Leaderboard', 'subTitle': 'Top Learners'}
    return render(request, 'placeholder.html', context)


@login_required
def my_badges(request):
    """My earned badges"""
    context = {'title': 'My Badges', 'subTitle': 'Achievements'}
    return render(request, 'placeholder.html', context)


@login_required
def achievements(request):
    """All achievements"""
    context = {'title': 'Achievements', 'subTitle': 'Milestones'}
    return render(request, 'placeholder.html', context)


@login_required
def student_profile(request):
    """Student profile view/edit"""
    context = {'title': 'My Profile', 'subTitle': 'Account Information'}
    return render(request, 'placeholder.html', context)


@login_required
def settings_account(request):
    """Account settings"""
    context = {'title': 'Settings', 'subTitle': 'Account'}
    return render(request, 'placeholder.html', context)


@login_required
def settings_preferences(request):
    """Learning preferences settings"""
    context = {'title': 'Settings', 'subTitle': 'Preferences'}
    return render(request, 'placeholder.html', context)


@login_required
def settings_notifications(request):
    """Notification settings"""
    context = {'title': 'Settings', 'subTitle': 'Notifications'}
    return render(request, 'placeholder.html', context)


@login_required
def notifications(request):
    """All notifications"""
    context = {'title': 'Notifications', 'subTitle': 'Recent Activity'}
    return render(request, 'placeholder.html', context)


def course_detail(request, slug):
    """Course detail page"""
    context = {'title': 'Course Details', 'subTitle': slug}
    return render(request, 'placeholder.html', context)
