from django.db import models
from django.contrib.auth.models import User


class Scenario(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "سهل"),
        ("medium", "متوسط"),
        ("hard", "صعب"),
    ]

    title = models.CharField(max_length=200, verbose_name="العنوان")
    slug = models.SlugField(unique=True, verbose_name="المعرف")
    description = models.TextField(verbose_name="الوصف")
    icon = models.CharField(max_length=10, verbose_name="الأيقونة")
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, verbose_name="الصعوبة"
    )

    # Stats
    capital = models.IntegerField(default=50, verbose_name="رأس المال")
    duration = models.CharField(max_length=50, default="10-15", verbose_name="المدة")
    age_range = models.CharField(
        max_length=50, default="8-12", verbose_name="الفئة العمرية"
    )

    # Rewards
    points_reward = models.IntegerField(default=50, verbose_name="مكافأة النقاط")
    coins_reward = models.IntegerField(default=25, verbose_name="مكافأة العملات")

    is_active = models.BooleanField(default=True, verbose_name="نشط")
    order = models.IntegerField(default=0, verbose_name="الترتيب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "سيناريو"
        verbose_name_plural = "السيناريوهات"

    def __str__(self):
        return self.title


class UserScenario(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتمل"),
        ("failed", "فشل"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_scenarios",
        verbose_name="المستخدم",
    )
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name="user_attempts",
        verbose_name="السيناريو",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
        verbose_name="الحالة",
    )
    score = models.IntegerField(default=0, verbose_name="النتيجة")
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="تاريخ الإكمال"
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ البدء")

    class Meta:
        ordering = ["-started_at"]
        verbose_name = "سيناريو المستخدم"
        verbose_name_plural = "سيناريوهات المستخدمين"

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title}"
