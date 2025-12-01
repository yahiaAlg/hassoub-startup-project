from django.core.management.base import BaseCommand
from accounts.models import Achievement
from scenarios.models import Scenario


class Command(BaseCommand):
    help = "Populate scenarios database with initial data"

    def handle(self, *args, **kwargs):
        scenarios_data = [
            {
                "title": "كشك الليمونادة الصيفي",
                "slug": "summer-lemonade-stand",
                "description": "ابدأ كشك الليمونادة الخاص بك! تعلم التكاليف الأساسية، التسعير، العرض والطلب، وصيغة الربح في بيئة صيفية منعشة.",
                "icon": "🍋",
                "difficulty": "easy",
                "capital": 50,
                "duration": "10-15",
                "age_range": "8-12",
                "points_reward": 100,
                "coins_reward": 50,
                "order": 1,
            },
            {
                "title": "قطب متجر الألعاب",
                "slug": "toy-store-tycoon",
                "description": "أدِر متجرألعاب ملون! تعلم التكاليف الثابتة والمتغيرة، إدارة المخزون، مزيج المنتجات، واقتصاديات الموقع.",
                "icon": "🧸",
                "difficulty": "medium",
                "capital": 200,
                "duration": "15-20",
                "age_range": "10-14",
                "points_reward": 150,
                "coins_reward": 75,
                "order": 2,
            },
            {
                "title": "رئيس المخبز المزدحم",
                "slug": "busy-bakery-boss",
                "description": "قم بإدارة مخبز دافئ ولذيذ! تعلم تخطيط الإنتاج، تحليل الوقت، الجودة مقابل الكمية، والعمليات اليومية.",
                "icon": "🧁",
                "difficulty": "medium",
                "capital": 150,
                "duration": "12-18",
                "age_range": "9-13",
                "points_reward": 130,
                "coins_reward": 65,
                "order": 3,
            },
            {
                "title": "كشك المزرعة الطازجة",
                "slug": "farm-fresh-stand",
                "description": "أدِر كشك مزرعة طبيعي! تعلم القيمة الزمنية للمال، تكلفة الفرصة البديلة، الطلب الموسمي، عوائد الاستثمار، وإدارة المخاطر.",
                "icon": "🌾",
                "difficulty": "hard",
                "capital": 100,
                "duration": "20-25",
                "age_range": "11-15",
                "points_reward": 180,
                "coins_reward": 90,
                "order": 4,
            },
            {
                "title": "غسيل السيارات المتنقل",
                "slug": "mobile-car-wash",
                "description": "قدم خدمة غسيل سيارات احترافية! تعلم تسعير الخدمات، قيمة عمر العميل، الجودة مقابل السرعة، والأعمال المتكررة.",
                "icon": "🚗",
                "difficulty": "medium",
                "capital": 80,
                "duration": "15-18",
                "age_range": "10-14",
                "points_reward": 120,
                "coins_reward": 60,
                "order": 5,
            },
            {
                "title": "خدمة رعاية الحيوانات الأليفة",
                "slug": "pet-sitting-service",
                "description": "اعتني بالحيوانات الأليفة الرائعة! تعلم إدارة الوقت، بناء السمعة، مزيج الخدمات، وقيود الجدولة.",
                "icon": "🐾",
                "difficulty": "easy",
                "capital": 40,
                "duration": "12-15",
                "age_range": "9-13",
                "points_reward": 90,
                "coins_reward": 45,
                "order": 6,
            },
            {
                "title": "متجر اللوازم المدرسية",
                "slug": "school-supplies-store",
                "description": "أدِر متجر لوازم مدرسية منظم! تعلم الطلب الموسمي، الشراء بالجملة، التوقيت، التسعير الديناميكي، ورأس المال العامل.",
                "icon": "📚",
                "difficulty": "medium",
                "capital": 300,
                "duration": "18-22",
                "age_range": "10-14",
                "points_reward": 160,
                "coins_reward": 80,
                "order": 7,
            },
            {
                "title": "متجر الحرف اليدوية الإلكتروني",
                "slug": "handmade-crafts-online-store",
                "description": "ابدأ متجراً إلكترونياً إبداعياً! تعلم قيمة العمل، التجارة الإلكترونية، التقييمات/السمعة، الوقت كمورد، وقيود التوسع.",
                "icon": "🎨",
                "difficulty": "hard",
                "capital": 100,
                "duration": "20-25",
                "age_range": "12-15",
                "points_reward": 200,
                "coins_reward": 100,
                "order": 8,
            },
            {
                "title": "خدمة إزالة الثلوج",
                "slug": "snow-removal-service",
                "description": "أدِر خدمة إزالة ثلوج شتوية! تعلم الأعمال المعتمدة على الطقس، العقود مقابل الطلب، إدارة المخاطر، وقيود القدرة.",
                "icon": "❄️",
                "difficulty": "hard",
                "capital": 120,
                "duration": "18-22",
                "age_range": "12-15",
                "points_reward": 170,
                "coins_reward": 85,
                "order": 9,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in scenarios_data:
            scenario, created = Scenario.objects.update_or_create(
                slug=data["slug"], defaults=data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ تم إنشاء السيناريو: {scenario.title}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"↻ تم تحديث السيناريو: {scenario.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ تم بنجاح! إنشاء: {created_count}، تحديث: {updated_count}"
            )
        )

        achievements = [
            {
                "name": "First Lemonade Stand",
                "name_ar": "أول كشك ليمونادة",
                "description": "Complete your first lemonade stand scenario",
                "description_ar": "أكمل سيناريو كشك الليمونادة للمرة الأولى",
                "icon": "🍋",
                "achievement_type": "scenario",
                "points_reward": 50,
                "coins_reward": 25,
            },
            {
                "name": "Perfect Business",
                "name_ar": "عمل مثالي",
                "description": "Score 100% on any scenario",
                "description_ar": "احصل على 100% في أي سيناريو",
                "icon": "💯",
                "achievement_type": "quiz",
                "points_reward": 100,
                "coins_reward": 50,
            },
            {
                "name": "Business Genius",
                "name_ar": "عبقري الأعمال",
                "description": "Score 90% or higher on a scenario",
                "description_ar": "احصل على 90% أو أكثر في سيناريو",
                "icon": "🧠",
                "achievement_type": "scenario",
                "points_reward": 75,
                "coins_reward": 35,
            },
            {
                "name": "5 Scenarios Master",
                "name_ar": "خبير 5 سيناريوهات",
                "description": "Complete 5 different scenarios",
                "description_ar": "أكمل 5 سيناريوهات مختلفة",
                "icon": "🏆",
                "achievement_type": "special",
                "points_reward": 200,
                "coins_reward": 100,
            },
            {
                "name": "Profit Master",
                "name_ar": "سيد الأرباح",
                "description": "Earn over $100 profit in lemonade stand",
                "description_ar": "اكسب أكثر من $100 ربح في كشك الليمونادة",
                "icon": "💰",
                "achievement_type": "scenario",
                "points_reward": 60,
                "coins_reward": 30,
            },
        ]

        for ach_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=ach_data["name"], defaults=ach_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created achievement: {achievement.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Achievement already exists: {achievement.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("✅ All achievements created successfully!")
        )
