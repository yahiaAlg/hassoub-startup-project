from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pages.models import (
    SiteSettings,
    TeamMember,
    FAQ,
    Testimonial,
    SiteStatistics,
    Offer,  # Add this
)


class Command(BaseCommand):
    help = "Populate pages app models with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to populate pages app..."))

        self.create_site_settings()
        self.create_statistics()
        self.create_faqs()
        self.create_testimonials()
        self.create_team_members()
        self.create_offers()  # Add this

        self.stdout.write(self.style.SUCCESS("Successfully populated pages app!"))

    def create_site_settings(self):
        """Create or update site settings"""
        settings, created = SiteSettings.objects.get_or_create(pk=1)

        settings.site_name = "BizVenture Kids"
        settings.site_name_ar = "بيزفينشر كيدز"
        settings.tagline = (
            "Play. Decide. Grow: The Safe Way to Learn Real Money Skills!"
        )
        settings.tagline_ar = (
            "العب. قرر. انمو: الطريقة الآمنة لتعلم مهارات المال الحقيقية!"
        )
        settings.phone = "+47 961 78 807"
        settings.email = "Info@BizVentureKids.no"
        settings.address = "Oslo, Norway"
        settings.address_ar = "أوسلو، النرويج"
        settings.facebook_url = "https://facebook.com/bizventurekids"
        settings.twitter_url = "https://twitter.com/bizventurekids"
        settings.instagram_url = "https://instagram.com/bizventurekids"
        settings.youtube_url = "https://youtube.com/bizventurekids"

        settings.about_text = """BizVenture Kids was founded in 2020 by a team of educators, parents, and financial experts 
        who noticed a critical gap in children's financial education. While schools teach math and basic economics, 
        most children graduate without understanding how to manage money in real-life situations, make informed spending 
        decisions, understand how businesses work, or develop entrepreneurial thinking.

        We set out to create a solution that would make financial education interactive, engaging, and relevant to children's 
        lives. Our simulations allow children to experience the excitement of running a business, the challenge of making 
        tough financial decisions, and the satisfaction of seeing their efforts pay off—all in a safe, game-like environment.

        Since our launch, we've helped thousands of children across more than 20 countries develop financial confidence 
        and business acumen. Our platform continues to grow with new simulations, learning paths, and educational resources."""

        settings.about_text_ar = """تم تأسيس بيزفينشر كيدز في عام 2020 من قبل فريق من المعلمين والآباء والخبراء الماليين 
        الذين لاحظوا وجود فجوة حرجة في التعليم المالي للأطفال. بينما تعلم المدارس الرياضيات والاقتصاد الأساسي، 
        يتخرج معظم الأطفال دون فهم كيفية إدارة الأموال في المواقف الحياتية الحقيقية، أو اتخاذ قرارات إنفاق مستنيرة، 
        أو فهم كيفية عمل الشركات، أو تطوير التفكير الريادي.

        شرعنا في إنشاء حل من شأنه أن يجعل التعليم المالي تفاعلياً وجذاباً وملائماً لحياة الأطفال. تتيح محاكاتنا 
        للأطفال تجربة إثارة إدارة عمل تجاري، وتحدي اتخاذ قرارات مالية صعبة، والرضا برؤية جهودهم تؤتي ثمارها—كل ذلك 
        في بيئة آمنة تشبه اللعبة.

        منذ إطلاقنا، ساعدنا آلاف الأطفال في أكثر من 20 دولة على تطوير الثقة المالية والفطنة التجارية. تستمر منصتنا 
        في النمو مع محاكاات جديدة ومسارات تعليمية وموارد تعليمية."""

        settings.mission = """At BizVenture Kids, we believe that financial literacy is one of the most important life skills 
        children can learn. Our mission is to make financial education engaging, practical, and fun for children ages 8-15 
        through interactive business simulations.

        We create safe, game-based learning environments where children can:
        - Manage virtual businesses and make real financial decisions
        - Learn about revenue, expenses, profit, and loss in a risk-free environment
        - Develop critical thinking and problem-solving skills
        - Gain confidence in making financial choices
        - Understand the value of money and resources

        Our simulations are designed to be age-appropriate, educational, and entertaining, helping children develop 
        essential money management skills that will serve them throughout their lives."""

        settings.mission_ar = """في بيزفينشر كيدز، نؤمن بأن الثقافة المالية هي واحدة من أهم المهارات الحياتية التي يمكن 
        للأطفال تعلمها. مهمتنا هي جعل التعليم المالي جذاباً وعملياً وممتعاً للأطفال الذين تتراوح أعمارهم بين 8-15 سنة 
        من خلال محاكاة الأعمال التفاعلية.

        نقوم بإنشاء بيئات تعليمية آمنة قائمة على الألعاب حيث يمكن للأطفال:
        - إدارة الأعمال الافتراضية واتخاذ قرارات مالية حقيقية
        - تعلم الإيرادات والنفقات والأرباح والخسائر في بيئة خالية من المخاطر
        - تطوير مهارات التفكير النقدي وحل المشكلات
        - اكتساب الثقة في اتخاذ الخيارات المالية
        - فهم قيمة المال والموارد

        تم تصميم محاكاتنا لتكون مناسبة للعمر، تعليمية، ومسلية، مما يساعد الأطفال على تطوير مهارات إدارة الأموال 
        الأساسية التي ستخدمهم طوال حياتهم."""

        settings.vision = """A world where every child grows up financially literate, confident, and ready to make smart 
        money decisions. We envision a future where financial education is accessible, engaging, and effective for all 
        children, regardless of their background or circumstances."""

        settings.vision_ar = """عالم يكبر فيه كل طفل ملماً بالمعرفة المالية، واثقاً، ومستعداً لاتخاذ قرارات مالية ذكية. 
        نتصور مستقبلاً حيث يكون التعليم المالي متاحاً وجذاباً وفعالاً لجميع الأطفال، بغض النظر عن خلفيتهم أو ظروفهم."""

        settings.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} Site Settings"))

    def create_statistics(self):
        """Create or update site statistics"""
        stats, created = SiteStatistics.objects.get_or_create(pk=1)

        stats.total_students = 12000
        stats.total_lessons = 45
        stats.total_scenarios = 28
        stats.certificates_issued = 8500
        stats.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} Site Statistics"))

    def create_faqs(self):
        """Create FAQ entries"""
        faqs_data = [
            {
                "question": "How can I create an account?",
                "question_ar": "كيف يمكنني إنشاء حساب؟",
                "answer": 'You can create an account by clicking the "Sign Up" button on our homepage and following the simple registration process.',
                "answer_ar": 'يمكنك إنشاء حساب من خلال النقر على زر "التسجيل" في صفحتنا الرئيسية واتباع عملية التسجيل البسيطة.',
                "category": "Account",
                "order": 1,
            },
            {
                "question": "What age group is BizVenture Kids suitable for?",
                "question_ar": "ما هي الفئة العمرية المناسبة لبيزفينشر كيدز؟",
                "answer": "BizVenture Kids is designed for children ages 5-13, with age-appropriate content for each group.",
                "answer_ar": "تم تصميم بيزفينشر كيدز للأطفال الذين تتراوح أعمارهم بين 5-13 سنة، مع محتوى مصمم خصيصاً لمختلف الفئات العمرية.",
                "category": "General",
                "order": 2,
            },
            {
                "question": "Is real money involved?",
                "question_ar": "هل هناك أموال حقيقية متضمنة؟",
                "answer": "No! All activities use virtual currency. Children learn real financial skills in a completely safe environment.",
                "answer_ar": "لا! جميع الأنشطة تستخدم عملة افتراضية. يتعلم الأطفال مهارات مالية حقيقية في بيئة آمنة تماماً.",
                "category": "Safety",
                "order": 3,
            },
            {
                "question": "Is BizVenture Kids free?",
                "question_ar": "هل بيزفينشر كيدز مجاني؟",
                "answer": "Yes, BizVenture Kids offers basic features for free. We also have premium options for additional content and features.",
                "answer_ar": "نعم، يقدم بيزفينشر كيدز ميزات أساسية مجانية. لدينا أيضاً خيارات مميزة للحصول على محتوى وميزات إضافية.",
                "category": "Pricing",
                "order": 4,
            },
            {
                "question": "Can parents track their child's progress?",
                "question_ar": "هل يمكن للآباء تتبع تقدم أطفالهم؟",
                "answer": "Yes! Parents have access to a dedicated dashboard showing their child's progress, achievements, and learning milestones.",
                "answer_ar": "نعم! يتمتع الآباء بإمكانية الوصول إلى لوحة معلومات مخصصة تعرض تقدم أطفالهم وإنجازاتهم ومعالم التعلم.",
                "category": "Features",
                "order": 5,
            },
            {
                "question": "How can I reset my password?",
                "question_ar": "كيف يمكنني إعادة تعيين كلمة المرور الخاصة بي؟",
                "answer": 'You can reset your password by clicking the "Forgot Password?" link on the login page.',
                "answer_ar": 'يمكنك إعادة تعيين كلمة المرور الخاصة بك من خلال النقر على رابط "هل نسيت كلمة المرور؟" في صفحة تسجيل الدخول.',
                "category": "Account",
                "order": 6,
            },
        ]

        created_count = 0
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data["question"], defaults=faq_data
            )
            if created:
                created_count += 1
            else:
                for key, value in faq_data.items():
                    setattr(faq, key, value)
                faq.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/Updated {len(faqs_data)} FAQs ({created_count} new)"
            )
        )

    def create_testimonials(self):
        """Create testimonial entries"""
        testimonials_data = [
            {
                "name": "سارة أحمد",
                "role": "Mother of two",
                "role_ar": "أم لطفلين",
                "content": "My kids love BizVenture Kids! They've learned so much about saving and making smart choices. I highly recommend it!",
                "content_ar": "أطفالي يحبون بيزفينشر كيدز! لقد تعلموا الكثير عن الادخار واتخاذ خيارات ذكية. أوصي به بشدة!",
                "rating": 5,
            },
            {
                "name": "السيدة طومسون",
                "role": "5th Grade Teacher, Chicago",
                "role_ar": "معلمة الصف الخامس، شيكاغو",
                "content": "BizVenture Kids has changed the way my students engage with financial concepts. The simulations make abstract ideas tangible and fun!",
                "content_ar": "لقد غيرت بيزفينشر كيدز الطريقة التي يتفاعل بها طلابي مع المفاهيم المالية. تجعل المحاكاات الأفكار المجردة ملموسة وممتعة!",
                "rating": 5,
            },
            {
                "name": "كارلوس م.",
                "role": "Parent, Miami",
                "role_ar": "ولي أمر، ميامي",
                "content": "My son used to think money was just for spending, but after using BizVenture Kids, he started talking about saving and investing!",
                "content_ar": "كان ابني يعتقد أن المال مخصص للإنفاق فقط، ولكن بعد استخدام بيزفينشر كيدز، بدأ يتحدث عن الادخار والاستثمار!",
                "rating": 5,
            },
            {
                "name": "عائشة ك.",
                "role": "Student, Age 12",
                "role_ar": "طالبة، العمر 12",
                "content": "I love how the simulations let me try different business ideas without worrying about losing real money. It's like having my own company!",
                "content_ar": "أحب كيف تتيح لي المحاكاات تجربة أفكار عمل مختلفة دون القلق بشأن خسارة المال الحقيقي. إنه مثل امتلاك شركتي الخاصة!",
                "rating": 5,
            },
            {
                "name": "جيمس و.",
                "role": "Financial Advisor, New York",
                "role_ar": "مستشار مالي، نيويورك",
                "content": "As a financial advisor, I wish I had something like BizVenture Kids when I was growing up. I recommend it to all my clients with children.",
                "content_ar": "كمستشار مالي، أتمنى لو كان لدي شيء مثل بيزفينشر كيدز عندما كنت أكبر. أوصي به لجميع عملائي الذين لديهم أطفال.",
                "rating": 5,
            },
            {
                "name": "فاطمة حسن",
                "role": "Teacher and parent",
                "role_ar": "معلمة وأم",
                "content": "As an educator, I appreciate the thoughtful curriculum. As a parent, I love seeing my son engaged and learning!",
                "content_ar": "كمعلمة، أقدر المنهج المدروس. كأم، أحب رؤية ابني منخرطاً ومتعلماً!",
                "rating": 5,
            },
        ]

        created_count = 0
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data["name"], defaults=testimonial_data
            )
            if created:
                created_count += 1
            else:
                for key, value in testimonial_data.items():
                    setattr(testimonial, key, value)
                testimonial.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/Updated {len(testimonials_data)} Testimonials ({created_count} new)"
            )
        )

    def create_team_members(self):
        """Create team member profiles"""
        team_data = [
            {
                "username": "sarah_johnson",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.johnson@bizventurekids.no",
                "position": "Founder & CEO",
                "position_ar": "المؤسس والرئيس التنفيذي",
                "bio": "Former elementary school teacher with 15 years of experience educating children. Passionate about making learning fun and accessible.",
                "bio_ar": "معلمة سابقة في المدارس الابتدائية مع 15 عاماً من الخبرة في تعليم الأطفال. متحمسة لجعل التعلم ممتعاً ومتاحاً.",
                "specialization": "Educational Leadership",
                "specialization_ar": "القيادة التعليمية",
                "years_of_experience": 15,
                "order": 1,
            },
            {
                "username": "michael_chen",
                "first_name": "Michael",
                "last_name": "Chen",
                "email": "michael.chen@bizventurekids.no",
                "position": "CTO & Game Designer",
                "position_ar": "المدير التقني ومصمم الألعاب",
                "bio": "Expert in game development with a background in educational technology. Specializes in creating engaging learning experiences.",
                "bio_ar": "خبير في تطوير الألعاب مع خلفية في التكنولوجيا التعليمية. متخصص في إنشاء تجارب تعليمية جذابة.",
                "specialization": "Game Development & EdTech",
                "specialization_ar": "تطوير الألعاب والتكنولوجيا التعليمية",
                "years_of_experience": 12,
                "order": 2,
            },
            {
                "username": "emily_rodriguez",
                "first_name": "Emily",
                "last_name": "Rodriguez",
                "email": "emily.rodriguez@bizventurekids.no",
                "position": "Curriculum Director",
                "position_ar": "مديرة المناهج",
                "bio": "Financial educator with a Master's in Child Development. Designs our age-appropriate financial lessons.",
                "bio_ar": "مربية مالية حاصلة على ماجستير في تنمية الطفولة. تصمم دروسنا المالية المناسبة للعمر.",
                "specialization": "Financial Education",
                "specialization_ar": "التعليم المالي",
                "years_of_experience": 10,
                "order": 3,
            },
            {
                "username": "david_kim",
                "first_name": "David",
                "last_name": "Kim",
                "email": "david.kim@bizventurekids.no",
                "position": "Financial Expert",
                "position_ar": "خبير مالي",
                "bio": "Former investment banker turned educator. Ensures our simulations reflect real financial principles.",
                "bio_ar": "مصرفي استثماري سابق أصبح معلماً. يضمن أن محاكاتنا تعكس المبادئ المالية الحقيقية.",
                "specialization": "Finance & Economics",
                "specialization_ar": "المالية والاقتصاد",
                "years_of_experience": 18,
                "order": 4,
            },
        ]

        created_count = 0
        for member_data in team_data:
            username = member_data.pop("username")
            email = member_data.pop("email")
            first_name = member_data.pop("first_name")
            last_name = member_data.pop("last_name")

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                },
            )

            team_member, created = TeamMember.objects.get_or_create(
                user=user, defaults=member_data
            )

            if created:
                created_count += 1
            else:
                for key, value in member_data.items():
                    setattr(team_member, key, value)
                team_member.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/Updated {len(team_data)} Team Members ({created_count} new)"
            )
        )

    def create_offers(self):
        """Create offer entries"""
        offers_data = [
            {
                "name": "Premium Lemonade Stand",
                "name_ar": "كشك الليمون المميز",
                "category": "Virtual Business",
                "category_ar": "الأعمال الافتراضية",
                "icon": "🍋",
                "old_price": 750,
                "new_price": 560,
                "discount_percentage": 25,
                "rating": 5,
                "order": 1,
            },
            {
                "name": "Money Master Badge",
                "name_ar": "شارة سيد المال",
                "category": "Badges & Rewards",
                "category_ar": "شارات ومكافآت",
                "icon": "🏅",
                "old_price": 350,
                "new_price": 300,
                "discount_percentage": 15,
                "rating": 5,
                "order": 2,
            },
            {
                "name": "Business Adventure Map",
                "name_ar": "خريطة مغامرة الأعمال",
                "category": "Games & Tools",
                "category_ar": "الألعاب والأدوات",
                "icon": "🗺️",
                "old_price": 1026,
                "new_price": 720,
                "discount_percentage": 30,
                "rating": 5,
                "order": 3,
            },
            {
                "name": "Super Saver Plushie",
                "name_ar": "دمية المدخر الخارق",
                "category": "Rewards",
                "category_ar": "مكافآت",
                "icon": "🧸",
                "old_price": 637,
                "new_price": 510,
                "discount_percentage": 20,
                "rating": 5,
                "order": 4,
            },
        ]

        created_count = 0
        for offer_data in offers_data:
            offer, created = Offer.objects.get_or_create(
                name=offer_data["name"], defaults=offer_data
            )
            if created:
                created_count += 1
            else:
                for key, value in offer_data.items():
                    setattr(offer, key, value)
                offer.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/Updated {len(offers_data)} Offers ({created_count} new)"
            )
        )
