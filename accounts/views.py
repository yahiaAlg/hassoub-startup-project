from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg
from .models import ParentProfile, Achievement, UserAchievement, DailyStreak
from lessons.models import UserLesson, UserQuizAttempt, Certificate
from scenarios.models import UserScenario
from datetime import timedelta


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("accounts:user_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        password2 = request.POST.get("password2", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        age = request.POST.get("age", "").strip()
        parent_name = request.POST.get("parent_name", "").strip()
        parent_email = request.POST.get("parent_email", "").strip()
        parent_phone = request.POST.get("parent_phone", "").strip()
        is_parent = request.POST.get("is_parent") == "on"

        # Validation
        if not username or not email or not password:
            messages.error(
                request, "اسم المستخدم والبريد الإلكتروني وكلمة المرور مطلوبة!"
            )
            return redirect("accounts:register")

        if password != password2:
            messages.error(request, "كلمتا المرور غير متطابقتين!")
            return redirect("accounts:register")

        if len(password) < 6:
            messages.error(request, "يجب أن تكون كلمة المرور 6 أحرف على الأقل!")
            return redirect("accounts:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "اسم المستخدم موجود بالفعل!")
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني موجود بالفعل!")
            return redirect("accounts:register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Update profile
        profile = user.profile
        if age:
            profile.age = int(age)
        profile.parent_name = parent_name
        profile.parent_email = parent_email
        profile.parent_phone = parent_phone
        profile.save()

        # Create parent profile if needed
        if is_parent:
            ParentProfile.objects.create(user=user)

        # Create streak tracker
        DailyStreak.objects.create(user=user, current_streak=1, longest_streak=1)

        # Log the user in
        login(request, user)
        messages.success(request, f"مرحباً {username}! تم إنشاء حسابك بنجاح.")

        if is_parent:
            return redirect("accounts:parent_dashboard")
        return redirect("accounts:user_dashboard")

    return render(request, "accounts/signup-ar.html")


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect("accounts:user_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "اسم المستخدم وكلمة المرور مطلوبان!")
            return redirect("accounts:login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Update last login
            profile = user.profile
            profile.last_login_at = timezone.now()
            profile.save()

            # Update streak
            update_user_streak(user)

            messages.success(request, f"مرحباً بعودتك {user.first_name or username}!")

            # Redirect based on user type
            if hasattr(user, "parent_profile"):
                return redirect("accounts:parent_dashboard")

            next_page = request.GET.get("next")
            if next_page:
                return redirect(next_page)
            return redirect("accounts:user_dashboard")
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة!")
            return redirect("accounts:login")

    return render(request, "accounts/login-ar.html")


def update_user_streak(user):
    """Update user's daily streak"""
    streak, created = DailyStreak.objects.get_or_create(user=user)

    today = timezone.now().date()
    last_activity = streak.last_activity_date

    if last_activity == today:
        return  # Already counted today

    yesterday = today - timedelta(days=1)

    if last_activity == yesterday:
        # Continue streak
        streak.current_streak += 1
    elif last_activity < yesterday:
        # Streak broken, reset
        streak.current_streak = 1

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_activity_date = today
    streak.save()


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح!")
    return redirect("pages:index")


@login_required
def profile(request):
    """User profile view with edit capability"""
    profile = request.user.profile

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            # Update user info
            request.user.first_name = request.POST.get("first_name", "").strip()
            request.user.last_name = request.POST.get("last_name", "").strip()
            request.user.email = request.POST.get("email", "").strip()
            request.user.save()

            # Update profile
            age = request.POST.get("age", "").strip()
            if age:
                profile.age = int(age)

            profile.phone = request.POST.get("phone", "").strip()
            profile.bio = request.POST.get("bio", "").strip()
            profile.city = request.POST.get("city", "").strip()
            profile.gender = request.POST.get("gender", "")
            profile.parent_name = request.POST.get("parent_name", "").strip()
            profile.parent_email = request.POST.get("parent_email", "").strip()
            profile.parent_phone = request.POST.get("parent_phone", "").strip()

            # Handle avatar upload
            if "avatar" in request.FILES:
                profile.avatar = request.FILES["avatar"]

            profile.save()
            messages.success(request, "تم تحديث ملفك الشخصي بنجاح!")
            return redirect("accounts:profile")

        elif action == "change_password":
            old_password = request.POST.get("old_password", "").strip()
            new_password = request.POST.get("new_password", "").strip()
            confirm_password = request.POST.get("confirm_password", "").strip()

            if not request.user.check_password(old_password):
                messages.error(request, "كلمة المرور القديمة غير صحيحة!")
                return redirect("accounts:profile")

            if new_password != confirm_password:
                messages.error(request, "كلمات المرور الجديدة غير متطابقة!")
                return redirect("accounts:profile")

            if len(new_password) < 6:
                messages.error(request, "يجب أن تكون كلمة المرور 6 أحرف على الأقل!")
                return redirect("accounts:profile")

            request.user.set_password(new_password)
            request.user.save()
            login(request, request.user)

            messages.success(request, "تم تغيير كلمة المرور بنجاح!")
            return redirect("accounts:profile")
        elif action == "delete_account":
            # Delete user account
            username = request.user.username
            request.user.delete()
            logout(request)
            messages.success(request, f"تم حذف حساب {username} بنجاح.")
            return redirect("pages:index")

    # Get user achievements
    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related("achievement")

    # Get user stats
    completed_lessons = UserLesson.objects.filter(
        user=request.user, is_completed=True
    ).count()
    in_progress_lessons = UserLesson.objects.filter(
        user=request.user, is_completed=False
    ).count()
    completed_scenarios = UserScenario.objects.filter(
        user=request.user, status="completed"
    ).count()
    certificates = Certificate.objects.filter(user=request.user).count()

    # Get streak info
    streak = DailyStreak.objects.filter(user=request.user).first()

    context = {
        "profile": profile,
        "achievements": user_achievements,
        "completed_lessons": completed_lessons,
        "in_progress_lessons": in_progress_lessons,
        "completed_scenarios": completed_scenarios,
        "certificates": certificates,
        "streak": streak,
    }
    return render(request, "accounts/profile-ar.html", context)


@login_required
def user_dashboard(request):
    """Main user dashboard"""
    profile = request.user.profile

    # Recent lessons
    recent_lessons = (
        UserLesson.objects.filter(user=request.user)
        .select_related("lesson", "lesson__path")
        .order_by("-started_at")[:5]
    )

    # Recent scenarios
    recent_scenarios = (
        UserScenario.objects.filter(user=request.user)
        .select_related("scenario")
        .order_by("-started_at")[:5]
    )

    # Recent achievements
    recent_achievements = (
        UserAchievement.objects.filter(user=request.user)
        .select_related("achievement")
        .order_by("-earned_at")[:5]
    )

    # Statistics
    total_lessons = UserLesson.objects.filter(
        user=request.user, is_completed=True
    ).count()
    total_scenarios = UserScenario.objects.filter(
        user=request.user, status="completed"
    ).count()
    total_points = profile.total_points
    total_coins = profile.coins

    # Quiz stats
    quiz_attempts = UserQuizAttempt.objects.filter(user=request.user)
    avg_quiz_score = quiz_attempts.aggregate(avg=Avg("percentage"))["avg"] or 0

    # Certificates
    certificates = Certificate.objects.filter(user=request.user).select_related("path")

    # Streak
    streak = DailyStreak.objects.filter(user=request.user).first()

    context = {
        "profile": profile,
        "recent_lessons": recent_lessons,
        "recent_scenarios": recent_scenarios,
        "recent_achievements": recent_achievements,
        "total_lessons": total_lessons,
        "total_scenarios": total_scenarios,
        "total_points": total_points,
        "total_coins": total_coins,
        "avg_quiz_score": int(avg_quiz_score),
        "certificates": certificates,
        "streak": streak,
    }

    return render(request, "accounts/dashboard-ar.html", context)


@login_required
def progress_rewards(request):
    """Progress and rewards page"""
    profile = request.user.profile

    # All achievements with earned status
    all_achievements = Achievement.objects.filter(is_active=True).order_by(
        "order", "name"
    )
    user_achievement_ids = UserAchievement.objects.filter(
        user=request.user
    ).values_list("achievement_id", flat=True)

    achievements_data = []
    for achievement in all_achievements:
        is_earned = achievement.id in user_achievement_ids
        achievements_data.append(
            {
                "achievement": achievement,
                "is_earned": is_earned,
            }
        )

    # Level progress
    next_level_points = 0
    current_level = profile.level

    if current_level == 1:
        next_level_points = 100
    elif current_level == 2:
        next_level_points = 300
    elif current_level == 3:
        next_level_points = 600
    elif current_level == 4:
        next_level_points = 1000
    elif current_level == 5:
        next_level_points = 2000
    else:
        next_level_points = 2000 + (current_level - 5) * 500

    progress_percentage = profile.get_progress_to_next_level()

    # Recent achievements (last 10)
    recent_achievements = (
        UserAchievement.objects.filter(user=request.user)
        .select_related("achievement")
        .order_by("-earned_at")[:10]
    )

    # Streak info
    streak = DailyStreak.objects.filter(user=request.user).first()

    context = {
        "profile": profile,
        "achievements_data": achievements_data,
        "next_level_points": next_level_points,
        "progress_percentage": progress_percentage,
        "recent_achievements": recent_achievements,
        "streak": streak,
    }

    return render(request, "accounts/progress-rewards-ar.html", context)


@login_required
def parent_dashboard(request):
    """Parent dashboard to monitor children's progress"""
    if not hasattr(request.user, "parent_profile"):
        messages.error(request, "ليس لديك صلاحية الوصول إلى لوحة التحكم للآباء!")
        return redirect("accounts:user_dashboard")

    parent_profile = request.user.parent_profile
    children = parent_profile.children.all()

    children_data = []
    for child in children:
        child_profile = child.profile

        # Get child stats
        completed_lessons = UserLesson.objects.filter(
            user=child, is_completed=True
        ).count()
        completed_scenarios = UserScenario.objects.filter(
            user=child, status="completed"
        ).count()
        total_points = child_profile.total_points
        certificates = Certificate.objects.filter(user=child).count()

        # Recent activity
        recent_lessons = UserLesson.objects.filter(user=child).order_by("-started_at")[
            :3
        ]
        recent_achievements = UserAchievement.objects.filter(user=child).order_by(
            "-earned_at"
        )[:3]

        # Streak
        streak = DailyStreak.objects.filter(user=child).first()

        children_data.append(
            {
                "child": child,
                "profile": child_profile,
                "completed_lessons": completed_lessons,
                "completed_scenarios": completed_scenarios,
                "total_points": total_points,
                "certificates": certificates,
                "recent_lessons": recent_lessons,
                "recent_achievements": recent_achievements,
                "streak": streak,
            }
        )

    context = {
        "parent_profile": parent_profile,
        "children_data": children_data,
    }

    return render(request, "accounts/parent-dashboard-ar.html", context)


@login_required
def add_child(request):
    """Add a child to parent's account"""
    if not hasattr(request.user, "parent_profile"):
        messages.error(request, "ليس لديك صلاحية الوصول إلى هذه الصفحة!")
        return redirect("accounts:user_dashboard")

    if request.method == "POST":
        child_username = request.POST.get("child_username", "").strip()

        try:
            child = User.objects.get(username=child_username)
            parent_profile = request.user.parent_profile

            if child in parent_profile.children.all():
                messages.warning(request, "هذا الطفل مضاف بالفعل!")
            else:
                parent_profile.children.add(child)
                messages.success(request, f"تمت إضافة {child.get_full_name()} بنجاح!")
        except User.DoesNotExist:
            messages.error(request, "المستخدم غير موجود!")

    return redirect("accounts:parent_dashboard")


@login_required
def remove_child(request, child_id):
    """Remove a child from parent's account"""
    if not hasattr(request.user, "parent_profile"):
        messages.error(request, "ليس لديك صلاحية الوصول إلى هذه الصفحة!")
        return redirect("accounts:user_dashboard")

    if request.method == "POST":
        child = get_object_or_404(User, id=child_id)
        parent_profile = request.user.parent_profile
        parent_profile.children.remove(child)
        messages.success(request, f"تمت إزالة {child.get_full_name()} من قائمتك!")

    return redirect("accounts:parent_dashboard")
