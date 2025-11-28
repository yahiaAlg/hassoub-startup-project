from django.contrib import admin
from .models import Profile, ParentProfile, Achievement, UserAchievement, DailyStreak

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'level', 'total_points', 'coins', 'created_at']
    list_filter = ['level', 'gender', 'created_at']
    search_fields = ['user__username', 'user__email', 'parent_name']
    readonly_fields = ['created_at', 'updated_at', 'level']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'avatar', 'age', 'gender', 'date_of_birth', 'phone')
        }),
        ('Location', {
            'fields': ('city', 'country')
        }),
        ('Parent Info', {
            'fields': ('parent_name', 'parent_email', 'parent_phone', 'parent_relation')
        }),
        ('Gamification', {
            'fields': ('total_points', 'level', 'coins')
        }),
        ('Settings', {
            'fields': ('receive_notifications', 'receive_emails', 'language_preference')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'last_login_at')
        }),
    )


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'occupation', 'report_frequency', 'created_at']
    list_filter = ['report_frequency', 'created_at']
    search_fields = ['user__username', 'user__email']
    filter_horizontal = ['children']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'achievement_type', 'points_required', 'points_reward', 'coins_reward', 'is_active']
    list_filter = ['achievement_type', 'is_active']
    search_fields = ['name', 'description', 'name_ar', 'description_ar']
    list_editable = ['is_active', 'points_reward', 'coins_reward']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['earned_at', 'achievement__achievement_type']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['earned_at']


@admin.register(DailyStreak)
class DailyStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_activity_date']
    list_filter = ['last_activity_date']
    search_fields = ['user__username']
    readonly_fields = ['last_activity_date']