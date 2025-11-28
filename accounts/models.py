from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Norway')
    
    # Parent/Guardian info
    parent_name = models.CharField(max_length=100, blank=True)
    parent_email = models.EmailField(blank=True)
    parent_phone = models.CharField(max_length=20, blank=True)
    parent_relation = models.CharField(max_length=50, blank=True)  # Mother, Father, Guardian
    
    # Gamification
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)
    
    # Settings
    receive_notifications = models.BooleanField(default=True)
    receive_emails = models.BooleanField(default=True)
    language_preference = models.CharField(max_length=10, default='ar')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def calculate_level(self):
        """Calculate level based on total points"""
        if self.total_points < 100:
            return 1
        elif self.total_points < 300:
            return 2
        elif self.total_points < 600:
            return 3
        elif self.total_points < 1000:
            return 4
        elif self.total_points < 2000:
            return 5
        else:
            return min(10, 5 + (self.total_points - 2000) // 500)
    
    def save(self, *args, **kwargs):
        self.level = self.calculate_level()
        super().save(*args, **kwargs)
    
    def get_progress_to_next_level(self):
        """Get percentage progress to next level"""
        current_level = self.level
        if current_level == 1:
            return int((self.total_points / 100) * 100)
        elif current_level == 2:
            return int(((self.total_points - 100) / 200) * 100)
        elif current_level == 3:
            return int(((self.total_points - 300) / 300) * 100)
        elif current_level == 4:
            return int(((self.total_points - 600) / 400) * 100)
        else:
            return int(((self.total_points - 1000) / 500) * 100)


class ParentProfile(models.Model):
    """Separate profile for parent users to monitor their children"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    phone = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    children = models.ManyToManyField(User, related_name='parent_guardians', blank=True)
    receive_progress_reports = models.BooleanField(default=True)
    report_frequency = models.CharField(
        max_length=20,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='weekly'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Parent"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('lesson', 'Lesson Completion'),
        ('scenario', 'Scenario Completion'),
        ('streak', 'Daily Streak'),
        ('points', 'Points Milestone'),
        ('quiz', 'Quiz Perfect Score'),
        ('special', 'Special Achievement'),
    ]
    
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    description = models.TextField()
    description_ar = models.TextField()
    icon = models.CharField(max_length=10)
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    points_required = models.IntegerField(default=0)
    points_reward = models.IntegerField(default=10)
    coins_reward = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']
        ordering = ['-earned_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class DailyStreak(models.Model):
    """Track user's daily login streak"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"