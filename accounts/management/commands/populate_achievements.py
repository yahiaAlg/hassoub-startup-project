from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import (
    Profile,
    Achievement,
    UserAchievement,
    DailyStreak,
    ParentProfile,
)
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Populate initial achievements and sample data for accounts app"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating achievements...")

        # Create achievements matching the dashboard hardcoded data
        achievements_data = [
            {
                "name": "First Profit",
                "name_ar": "أول ربح",
                "description": "Earn your first profit",
                "description_ar": "احصل على أول ربح لك",
                "icon": "💰",
                "achievement_type": "special",
                "points_required": 0,
                "points_reward": 10,
                "coins_reward": 5,
                "order": 1,
            },
            {
                "name": "Lemonade Expert",
                "name_ar": "خبير الليمون",
                "description": "Master the lemonade stand",
                "description_ar": "أتقن كشك الليمون",
                "icon": "🍋",
                "achievement_type": "scenario",
                "points_required": 0,
                "points_reward": 25,
                "coins_reward": 10,
                "order": 2,
            },
            {
                "name": "Toy Tycoon",
                "name_ar": "قطب الألعاب",
                "description": "Build a successful toy empire",
                "description_ar": "بناء إمبراطورية ألعاب ناجحة",
                "icon": "🏆",
                "achievement_type": "scenario",
                "points_required": 0,
                "points_reward": 50,
                "coins_reward": 25,
                "order": 3,
            },
            {
                "name": "The Investor",
                "name_ar": "المستثمر",
                "description": "Make your first investment",
                "description_ar": "قم بأول استثمار لك",
                "icon": "📈",
                "achievement_type": "special",
                "points_required": 0,
                "points_reward": 30,
                "coins_reward": 15,
                "order": 4,
            },
            {
                "name": "7-Day Streak",
                "name_ar": "سلسلة 7 أيام",
                "description": "Login for 7 consecutive days",
                "description_ar": "سجل دخول لمدة 7 أيام متتالية",
                "icon": "🕒",
                "achievement_type": "streak",
                "points_required": 0,
                "points_reward": 40,
                "coins_reward": 20,
                "order": 5,
            },
            {
                "name": "Entrepreneur",
                "name_ar": "رجل أعمال",
                "description": "Complete 10 business scenarios",
                "description_ar": "أكمل 10 سيناريوهات تجارية",
                "icon": "🏢",
                "achievement_type": "scenario",
                "points_required": 0,
                "points_reward": 100,
                "coins_reward": 50,
                "order": 6,
            },
            {
                "name": "First Steps",
                "name_ar": "الخطوات الأولى",
                "description": "Complete your first lesson",
                "description_ar": "أكمل أول درس",
                "icon": "🎯",
                "achievement_type": "lesson",
                "points_required": 0,
                "points_reward": 10,
                "coins_reward": 5,
                "order": 7,
            },
            {
                "name": "Getting Started",
                "name_ar": "البداية",
                "description": "Complete 5 lessons",
                "description_ar": "أكمل 5 دروس",
                "icon": "📚",
                "achievement_type": "lesson",
                "points_required": 0,
                "points_reward": 25,
                "coins_reward": 10,
                "order": 8,
            },
            {
                "name": "Lesson Master",
                "name_ar": "سيد الدروس",
                "description": "Complete 10 lessons",
                "description_ar": "أكمل 10 دروس",
                "icon": "📖",
                "achievement_type": "lesson",
                "points_required": 0,
                "points_reward": 50,
                "coins_reward": 25,
                "order": 9,
            },
            {
                "name": "Perfect Score",
                "name_ar": "النتيجة الكاملة",
                "description": "Get 100% on a quiz",
                "description_ar": "احصل على 100% في اختبار",
                "icon": "💯",
                "achievement_type": "quiz",
                "points_required": 0,
                "points_reward": 30,
                "coins_reward": 15,
                "order": 10,
            },
            {
                "name": "Points Collector",
                "name_ar": "جامع النقاط",
                "description": "Earn 100 points",
                "description_ar": "اجمع 100 نقطة",
                "icon": "⭐",
                "achievement_type": "points",
                "points_required": 100,
                "points_reward": 20,
                "coins_reward": 10,
                "order": 11,
            },
            {
                "name": "Points Champion",
                "name_ar": "بطل النقاط",
                "description": "Earn 500 points",
                "description_ar": "اجمع 500 نقطة",
                "icon": "🌟",
                "achievement_type": "points",
                "points_required": 500,
                "points_reward": 50,
                "coins_reward": 30,
                "order": 12,
            },
        ]

        created_count = 0
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data["name"], defaults=achievement_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"  Created: {achievement.name}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} achievements")
        )

        # Create demo user matching dashboard data (Ahmed)
        self.stdout.write("\nChecking for demo users...")
        demo_username = "ahmed"

        if not User.objects.filter(username=demo_username).exists():
            demo_user = User.objects.create_user(
                username=demo_username,
                email="ahmed@example.com",
                password="demo123",
                first_name="أحمد",
                last_name="المغامر",
            )

            # Update profile to match dashboard stats
            profile = demo_user.profile
            profile.age = 12
            profile.gender = "male"
            profile.city = "Setif"
            profile.country = "Algeria"
            profile.total_points = 6500  # Level 5, 65% to Level 6
            profile.coins = 125
            profile.bio = "أحب تعلم الإدارة المالية والأعمال!"
            profile.save()

            # Create 7-day streak to match dashboard
            DailyStreak.objects.create(
                user=demo_user,
                current_streak=7,
                longest_streak=10,
                last_activity_date=timezone.now().date(),
            )

            # Award matching achievements from dashboard
            earned_achievements = Achievement.objects.filter(
                name__in=[
                    "First Profit",
                    "Lemonade Expert",
                    "Toy Tycoon",
                    "7-Day Streak",
                    "First Steps",
                ]
            )

            # Create achievements with specific dates
            for i, achievement in enumerate(earned_achievements):
                UserAchievement.objects.create(
                    user=demo_user,
                    achievement=achievement,
                    earned_at=timezone.now()
                    - timedelta(days=(len(earned_achievements) - i)),
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created demo user: {demo_username} (password: demo123)"
                )
            )
            self.stdout.write(f"  Total Points: {profile.total_points}")
            self.stdout.write(f"  Level: {profile.level}")
            self.stdout.write(f"  Coins: {profile.coins}")
            self.stdout.write(f"  Streak: {7} days")
            self.stdout.write(f"  Achievements: {earned_achievements.count()}")
        else:
            self.stdout.write("Demo user already exists")

        # Create demo parent
        parent_username = "parent_fatima"
        if not User.objects.filter(username=parent_username).exists():
            parent_user = User.objects.create_user(
                username=parent_username,
                email="fatima@example.com",
                password="parent123",
                first_name="فاطمة",
                last_name="أحمد",
            )

            parent_profile = ParentProfile.objects.create(
                user=parent_user,
                phone="+213555123456",
                occupation="مهندسة",
                receive_progress_reports=True,
                report_frequency="weekly",
            )

            # Link demo child to parent
            if User.objects.filter(username=demo_username).exists():
                child_user = User.objects.get(username=demo_username)
                parent_profile.children.add(child_user)
                self.stdout.write(f"  Linked {demo_username} to parent")

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created demo parent: {parent_username} (password: parent123)"
                )
            )
        else:
            parent_user = User.objects.get(username=parent_username)
            parent_profile = parent_user.parent_profile

            # Link demo child if not already linked
            if User.objects.filter(username=demo_username).exists():
                child_user = User.objects.get(username=demo_username)
                if child_user not in parent_profile.children.all():
                    parent_profile.children.add(child_user)
                    self.stdout.write(f"  Linked {demo_username} to existing parent")

            self.stdout.write("Demo parent already exists")

        self.stdout.write(self.style.SUCCESS("\n✅ All done!"))
        self.stdout.write("\nYou can login with:")
        self.stdout.write("  Child Account - Username: ahmed, Password: demo123")
        self.stdout.write(
            "  Parent Account - Username: parent_fatima, Password: parent123"
        )
