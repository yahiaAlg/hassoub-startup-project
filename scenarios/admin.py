from django.contrib import admin
from .models import Scenario, UserScenario


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "difficulty",
        "capital",
        "duration",
        "points_reward",
        "coins_reward",
        "is_active",
        "order",
    ]
    list_filter = ["difficulty", "is_active"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_active", "order"]
    ordering = ["order", "title"]

    fieldsets = (
        (
            "معلومات أساسية",
            {"fields": ("title", "slug", "description", "icon", "difficulty")},
        ),
        ("الإحصائيات", {"fields": ("capital", "duration", "age_range")}),
        ("المكافآت", {"fields": ("points_reward", "coins_reward")}),
        ("الإعدادات", {"fields": ("is_active", "order")}),
    )


@admin.register(UserScenario)
class UserScenarioAdmin(admin.ModelAdmin):
    list_display = ["user", "scenario", "status", "score", "started_at", "completed_at"]
    list_filter = ["status", "scenario", "started_at"]
    search_fields = ["user__username", "scenario__title"]
    readonly_fields = ["started_at"]
    date_hierarchy = "started_at"

    fieldsets = (
        ("المعلومات", {"fields": ("user", "scenario", "status", "score")}),
        ("التواريخ", {"fields": ("started_at", "completed_at")}),
    )
