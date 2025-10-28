from django.contrib import admin
from .models import Badge, UserBadge, Level, Achievement, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'points_reward', 'created_at']
    list_filter = ['badge_type', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at', 'is_displayed']
    list_filter = ['badge', 'is_displayed', 'earned_at']
    search_fields = ['user__username', 'user__email', 'badge__name']
    readonly_fields = ['earned_at']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level_number', 'name', 'xp_required', 'color']
    ordering = ['level_number']
    search_fields = ['name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'achievement_type', 'points_earned', 'achieved_at']
    list_filter = ['achievement_type', 'achieved_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['achieved_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'period', 'rank', 'total_points', 'total_xp', 'updated_at']
    list_filter = ['period', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['updated_at']
    ordering = ['period', 'rank']
