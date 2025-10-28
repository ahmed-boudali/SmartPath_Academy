from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BadgeViewSet, UserBadgeViewSet, LevelViewSet,
    AchievementViewSet, LeaderboardViewSet
)

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'user-badges', UserBadgeViewSet, basename='user-badge')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('', include(router.urls)),
]
