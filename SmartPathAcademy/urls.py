"""
URL configuration for SmartPathAcademy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from rest_framework.decorators import api_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.dashboard_views import student_dashboard, course_list, api_root as dashboard_root
from accounts.placeholder_views import (
    my_courses, ai_chat, student_progress, leaderboard, my_badges,
    achievements, student_profile, settings_account, settings_preferences,
    settings_notifications, notifications
)
from courses.frontend_views import (
    course_detail, course_enroll, lesson_view, lesson_complete, quiz_take
)


@api_view(['GET'])
def api_index(request):
    """API Root - Welcome to SmartPath Academy API"""
    return JsonResponse({
        'message': 'Welcome to SmartPath Academy API',
        'version': '1.0',
        'endpoints': {
            'documentation': {
                'swagger': request.build_absolute_uri('/api/swagger/'),
                'redoc': request.build_absolute_uri('/api/redoc/'),
            },
            'admin': request.build_absolute_uri('/admin/'),
            'api': {
                'authentication': request.build_absolute_uri('/api/auth/'),
                'accounts': request.build_absolute_uri('/api/accounts/'),
                'courses': request.build_absolute_uri('/api/courses/'),
                'gamification': request.build_absolute_uri('/api/gamification/'),
                'ai_coach': request.build_absolute_uri('/api/ai-coach/'),
                'analytics': request.build_absolute_uri('/api/analytics/'),
            }
        },
        'status': 'online',
    })

schema_view = get_schema_view(
    openapi.Info(
        title="SmartPath Academy API",
        default_version='v1',
        description="API documentation for SmartPath Academy",
        terms_of_service="https://www.smartpathacademy.com/terms/",
        contact=openapi.Contact(email="contact@smartpathacademy.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Frontend Views
    path('', dashboard_root, name='index'),
    path('dashboard/', student_dashboard, name='student-dashboard'),
    
    # Authentication (moved to accounts.urls)
    path('accounts/', include('accounts.urls')),
    
    # Courses
    path('courses/', course_list, name='course-list'),
    path('courses/<slug:slug>/', course_detail, name='course-detail'),
    path('courses/<slug:slug>/enroll/', course_enroll, name='course-enroll'),
    path('lesson/<int:lesson_id>/', lesson_view, name='lesson-view'),
    path('lesson/<int:lesson_id>/complete/', lesson_complete, name='lesson-complete'),
    path('quiz/<int:quiz_id>/', quiz_take, name='quiz-take'),
    path('my-courses/', my_courses, name='my-courses'),
    
    # AI Coach
    path('ai-coach/', ai_chat, name='ai-chat'),
    
    # Analytics & Progress
    path('progress/', student_progress, name='student-progress'),
    
    # Gamification
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('my-badges/', my_badges, name='my-badges'),
    path('achievements/', achievements, name='achievements'),
    
    # Profile
    path('profile/', student_profile, name='student-profile'),
    
    # Settings
    path('settings/account/', settings_account, name='settings-account'),
    path('settings/preferences/', settings_preferences, name='settings-preferences'),
    path('settings/notifications/', settings_notifications, name='settings-notifications'),
    
    # Notifications
    path('notifications/', notifications, name='notifications'),
    
    # API Root
    path('api/', api_index, name='api-index'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai-coach/', include('ai_coach.urls')),
    path('api/analytics/', include('analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
