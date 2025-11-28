from django.db import models
from django.contrib.auth.models import User


class SiteSettings(models.Model):
    """Singleton model for site-wide settings"""

    site_name = models.CharField(max_length=100, default="BizVenture Kids")
    site_name_ar = models.CharField(max_length=100, default="بيزفينشر كيدز")
    tagline = models.CharField(max_length=200, blank=True)
    tagline_ar = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    address_ar = models.CharField(max_length=300)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="site/", blank=True)
    favicon = models.ImageField(upload_to="site/", blank=True)
    about_text = models.TextField(blank=True)
    about_text_ar = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    mission_ar = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    vision_ar = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class TeamMember(models.Model):
    """Team member profile linked to User model"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="team_profile"
    )
    position = models.CharField(max_length=100)
    position_ar = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    bio_ar = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    specialization_ar = models.CharField(max_length=200, blank=True)
    years_of_experience = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "user__first_name"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    reply_message = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    question_ar = models.CharField(max_length=300)
    answer = models.TextField()
    answer_ar = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    role_ar = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    content_ar = models.TextField(blank=True)
    rating = models.IntegerField(default=5)
    avatar = models.ImageField(upload_to="testimonials/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class SiteStatistics(models.Model):
    """Site statistics shown on homepage"""

    total_students = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    total_scenarios = models.IntegerField(default=0)
    certificates_issued = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Statistics"
        verbose_name_plural = "Site Statistics"

    def __str__(self):
        return f"Statistics - Updated {self.updated_at}"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_stats(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Offer(models.Model):
    """Special offers for products/services"""

    name = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    category_ar = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="🎁", help_text="Emoji icon")
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name
