from django.core.management.base import BaseCommand
from lessons.models import LearningPath, Lesson, Quiz, Question, Answer


class Command(BaseCommand):
    help = "Populate lessons database with initial learning path data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating learning path and lessons...")

        # Create Learning Path
        path, created = LearningPath.objects.get_or_create(
            title="مسار إتقان المال",
            defaults={
                "description": "أتقن أساسيات إدارة المال، من الادخار الأساسي إلى استراتيجيات الأعمال المتقدمة. أكمل جميع الدروس لتحصل على شهادة سيد المال الخاصة بك!",
                "icon": "💰",
                "difficulty": "intermediate",
                "min_age": 10,
                "max_age": 14,
                "total_duration": 480,  # 8 hours in minutes
                "certificate_available": True,
                "order": 1,
                "is_active": True,
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created learning path: {path.title}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Learning path already exists: {path.title}")
            )

        # Lessons data
        lessons_data = [
            {
                "title": "مقدمة في المال",
                "description": "تعرف على أنواع المال المختلفة، وكيفية استخدامه، ولماذا هو مهم في حياتنا اليومية.",
                "icon": "💰",
                "duration": 30,
                "order": 1,
                "content": "<h3>مرحباً بك في عالم المال!</h3><p>المال هو وسيلة التبادل التي نستخدمها لشراء السلع والخدمات...</p>",
                "points": 10,
                "coins": 5,
                "requires_previous": False,
            },
            {
                "title": "الادخار مقابل الإنفاق",
                "description": "استكشف الفرق بين الادخار والإنفاق، وتعلم استراتيجيات الإدارة الذكية للمال.",
                "icon": "💸",
                "duration": 45,
                "order": 2,
                "content": "<h3>الفرق بين الادخار والإنفاق</h3><p>الادخار يعني الاحتفاظ بالمال للمستقبل، بينما الإنفاق هو استخدام المال الآن...</p>",
                "points": 15,
                "coins": 8,
                "requires_previous": True,
            },
            {
                "title": "الميزانية الأساسية",
                "description": "أنشئ ميزانيتك الأولى وتعلم كيفية تتبع الدخل والمصروفات بفعالية.",
                "icon": "🛒",
                "duration": 60,
                "order": 3,
                "content": "<h3>كيفية إنشاء ميزانية</h3><p>الميزانية هي خطة لكيفية إنفاق أموالك. دعونا نتعلم كيفية إنشاء واحدة...</p>",
                "points": 20,
                "coins": 10,
                "requires_previous": True,
            },
            {
                "title": "محاكاة كشك الليموناضة",
                "description": "قم بإدارة كشك الليموناضة الافتراضي الخاص بك وتعلم عن التكاليف والتسعير والربح.",
                "icon": "🍋",
                "duration": 60,
                "order": 4,
                "content": "<h3>محاكاة عمل تجاري</h3><p>تخيل أنك تدير كشك ليموناضة. ستتعلم عن التكاليف والإيرادات والأرباح...</p>",
                "points": 25,
                "coins": 15,
                "requires_previous": True,
            },
            {
                "title": "قطب متجر الألعاب",
                "description": "قم بإدارة متجر ألعاب بمنتجات متعددة ومخزون وأنواع عملاء مختلفة.",
                "icon": "🧸",
                "duration": 90,
                "order": 5,
                "content": "<h3>إدارة متجر متقدمة</h3><p>الآن دعونا نتعامل مع عمل أكثر تعقيداً مع المخزون والعملاء المختلفين...</p>",
                "points": 30,
                "coins": 20,
                "requires_previous": True,
            },
            {
                "title": "فهم الربح",
                "description": "تعلم كيفية حساب الربح وفهم الفرق بين الإيرادات والمصروفات.",
                "icon": "📊",
                "duration": 45,
                "order": 6,
                "content": "<h3>ما هو الربح؟</h3><p>الربح = الإيرادات - المصروفات. دعونا نتعلم كيفية حسابه...</p>",
                "points": 20,
                "coins": 10,
                "requires_previous": True,
            },
            {
                "title": "مقدمة في الخدمات المصرفية",
                "description": "تعرف على الحسابات المصرفية والفوائد وكيف تساعد البنوك في إدارة المال.",
                "icon": "💳",
                "duration": 60,
                "order": 7,
                "content": "<h3>دور البنوك</h3><p>البنوك تساعد في الحفاظ على أموالنا آمنة وتنمو من خلال الفوائد...</p>",
                "points": 25,
                "coins": 15,
                "requires_previous": True,
            },
            {
                "title": "أساسيات الاستثمار",
                "description": "اكتشف أساسيات الاستثمار وكيف يمكن للمال أن ينمو بمرور الوقت.",
                "icon": "📈",
                "duration": 60,
                "order": 8,
                "content": "<h3>مقدمة للاستثمار</h3><p>الاستثمار يعني وضع أموالك للعمل لكسب المزيد من المال...</p>",
                "points": 30,
                "coins": 18,
                "requires_previous": True,
            },
            {
                "title": "تخطيط الأعمال",
                "description": "تعلم كيفية إنشاء خطة عمل وفهم مفاهيم الأعمال الرئيسية.",
                "icon": "🏢",
                "duration": 90,
                "order": 9,
                "content": "<h3>إنشاء خطة عمل</h3><p>خطة العمل هي خريطة طريق لعملك. دعونا نتعلم كيفية إنشاء واحدة...</p>",
                "points": 35,
                "coins": 20,
                "requires_previous": True,
            },
            {
                "title": "الميزانية المتقدمة",
                "description": "ارتق بمهارات الميزانية الخاصة بك إلى المستوى التالي باستخدام تقنيات وأدوات متقدمة.",
                "icon": "💼",
                "duration": 60,
                "order": 10,
                "content": "<h3>تقنيات الميزانية المتقدمة</h3><p>تعلم استراتيجيات أكثر تعقيداً لإدارة أموالك...</p>",
                "points": 30,
                "coins": 18,
                "requires_previous": True,
            },
            {
                "title": "تحليل السوق",
                "description": "فهم كيفية تحليل اتجاهات السوق واتخاذ قرارات عمل مستنيرة.",
                "icon": "📉",
                "duration": 60,
                "order": 11,
                "content": "<h3>فهم الأسواق</h3><p>تعلم كيفية قراءة اتجاهات السوق واتخاذ قرارات ذكية...</p>",
                "points": 30,
                "coins": 18,
                "requires_previous": True,
            },
            {
                "title": "إدارة المخاطر المالية",
                "description": "تعلم كيفية تحديد وإدارة المخاطر المالية في العمل والحياة الشخصية.",
                "icon": "⚠️",
                "duration": 90,
                "order": 12,
                "content": "<h3>إدارة المخاطر</h3><p>كل قرار مالي ينطوي على مخاطر. دعونا نتعلم كيفية إدارتها...</p>",
                "points": 35,
                "coins": 20,
                "requires_previous": True,
            },
            {
                "title": "المشروع النهائي",
                "description": "طبق كل ما تعلمته في مشروع عمل شامل واحصل على شهادتك.",
                "icon": "🎯",
                "duration": 120,
                "order": 13,
                "content": "<h3>مشروعك النهائي</h3><p>حان الوقت لتطبيق كل ما تعلمته في مشروع شامل...</p>",
                "points": 50,
                "coins": 30,
                "requires_previous": True,
            },
        ]

        # Create lessons
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                path=path,
                order=lesson_data["order"],
                defaults={
                    "title": lesson_data["title"],
                    "description": lesson_data["description"],
                    "icon": lesson_data["icon"],
                    "duration": lesson_data["duration"],
                    "content": lesson_data["content"],
                    "points": lesson_data["points"],
                    "coins": lesson_data["coins"],
                    "requires_previous": lesson_data["requires_previous"],
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ Created lesson {lesson.order}: {lesson.title}"
                    )
                )

                # Create a sample quiz for each lesson
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=f"اختبار: {lesson.title}",
                    description=f"اختبر معرفتك حول {lesson.title}",
                    pass_percentage=70,
                    is_active=True,
                )

                # Create sample questions
                sample_questions = [
                    {
                        "question_text": f"ما هو المفهوم الرئيسي في {lesson.title}؟",
                        "answers": [
                            {"text": "الإجابة الصحيحة", "is_correct": True},
                            {"text": "إجابة خاطئة 1", "is_correct": False},
                            {"text": "إجابة خاطئة 2", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": f"كيف يمكنك تطبيق ما تعلمته في {lesson.title}؟",
                        "answers": [
                            {"text": "من خلال الممارسة اليومية", "is_correct": True},
                            {"text": "بتجاهل المفاهيم", "is_correct": False},
                            {"text": "بعدم التفكير فيها", "is_correct": False},
                        ],
                    },
                ]

                for idx, q_data in enumerate(sample_questions, 1):
                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=q_data["question_text"],
                        question_type="multiple",
                        points=1,
                        order=idx,
                    )

                    for ans_idx, ans_data in enumerate(q_data["answers"], 1):
                        Answer.objects.create(
                            question=question,
                            answer_text=ans_data["text"],
                            is_correct=ans_data["is_correct"],
                            order=ans_idx,
                        )

                self.stdout.write(
                    f"    ✓ Created quiz with {len(sample_questions)} questions"
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠ Lesson already exists: {lesson.title}")
                )

        self.stdout.write(self.style.SUCCESS("\n✅ Successfully populated lessons!"))
        self.stdout.write(f"Total lessons created: {path.lessons.count()}")
