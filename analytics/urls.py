from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserActivityViewSet, QuizAttemptViewSet

router = DefaultRouter()
router.register(r'activities', UserActivityViewSet, basename='user-activity')
router.register(r'quiz-attempts', QuizAttemptViewSet, basename='quiz-attempt')

urlpatterns = [
    path('', include(router.urls)),
]
