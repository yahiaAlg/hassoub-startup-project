from django.contrib import admin
from .models import (
    SiteSettings, TeamMember, ContactMessage, 
    FAQ, Testimonial, SiteStatistics
)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('site_name', 'site_name_ar', 'tagline', 'tagline_ar', 'logo', 'favicon')
        }),
        ('Contact Info', {
            'fields': ('phone', 'email', 'address', 'address_ar')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('About Content', {
            'fields': ('about_text', 'about_text_ar', 'mission', 'mission_ar', 'vision', 'vision_ar')
        }),
    )
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'years_of_experience', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'position']
    list_editable = ['is_active', 'order']
    raw_id_fields = ['user']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read', 'replied']
    list_filter = ['is_read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'replied_at']
    
    fieldsets = (
        ('Message Info', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read', 'replied', 'reply_message', 'replied_at')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['question', 'answer', 'question_ar', 'answer_ar']
    list_editable = ['order', 'is_active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating', 'created_at']
    search_fields = ['name', 'role', 'content']
    list_editable = ['is_active']


@admin.register(SiteStatistics)
class SiteStatisticsAdmin(admin.ModelAdmin):
    list_display = ['total_students', 'total_lessons', 'total_scenarios', 'certificates_issued', 'updated_at']
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        return not SiteStatistics.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False