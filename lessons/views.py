from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import (
    LearningPath, Lesson, UserLesson, Quiz, Question, 
    Answer, UserQuizAttempt, Certificate
)
from accounts.models import UserAchievement, Achievement
import random
import string

@login_required
def learning_path(request):
    """Display the main learning path with integrated lesson content"""
    path = LearningPath.objects.filter(is_active=True).first()
    
    if not path:
        messages.error(request, 'لا توجد مسارات تعليمية متاحة حالياً.')
        return redirect('pages:index')
    
    # Get selected lesson if any
    selected_lesson_id = request.GET.get('lesson')
    selected_lesson = None
    quiz = None
    
    if selected_lesson_id:
        selected_lesson = get_object_or_404(Lesson, id=selected_lesson_id, is_active=True)
        if not selected_lesson.is_locked_for_user(request.user):
            quiz = selected_lesson.quizzes.filter(is_active=True).first()
            
            # Mark as started
            UserLesson.objects.get_or_create(
                user=request.user,
                lesson=selected_lesson
            )
    
    # Get all lessons for this path
    lessons = path.lessons.filter(is_active=True)
    
    # Get user progress for each lesson
    lessons_data = []
    for lesson in lessons:
        user_lesson = UserLesson.objects.filter(
            user=request.user,
            lesson=lesson
        ).first()
        
        is_locked = lesson.is_locked_for_user(request.user)
        
        if user_lesson and user_lesson.is_completed:
            status = 'completed'
        elif user_lesson and not user_lesson.is_completed:
            status = 'inprogress'
        elif is_locked:
            status = 'locked'
        else:
            status = 'unlocked'
        
        lessons_data.append({
            'lesson': lesson,
            'user_lesson': user_lesson,
            'status': status,
            'is_locked': is_locked,
        })
    
    # Calculate overall progress
    total_lessons = lessons.count()
    completed_lessons = UserLesson.objects.filter(
        user=request.user,
        lesson__path=path,
        is_completed=True
    ).count()
    
    progress_percentage = 0
    if total_lessons > 0:
        progress_percentage = int((completed_lessons / total_lessons) * 100)
    
    context = {
        'path': path,
        'lessons_data': lessons_data,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'progress_percentage': progress_percentage,
        'selected_lesson': selected_lesson,
        'quiz': quiz,
    }
    
    return render(request, 'lessons/learning_path.html', context)


@login_required
def complete_lesson(request, lesson_id):
    """Mark lesson as complete"""
    if request.method != 'POST':
        return redirect('lessons:learning_path')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    user_lesson, created = UserLesson.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    if not user_lesson.is_completed:
        user_lesson.is_completed = True
        user_lesson.completed_at = timezone.now()
        user_lesson.progress_percentage = 100
        user_lesson.save()
        
        # Award points and coins
        profile = request.user.profile
        profile.total_points += lesson.points
        profile.coins += lesson.coins
        profile.save()
        
        # Check for achievements
        check_lesson_achievements(request.user)
        
        messages.success(
            request, 
            f'تهانينا! لقد أكملت درس "{lesson.title}" وحصلت على {lesson.points} نقطة و {lesson.coins} عملة!'
        )
    
    return redirect('lessons:learning_path')


@login_required
def quiz_submit(request, quiz_id):
    """Submit quiz answers"""
    if request.method != 'POST':
        return redirect('lessons:learning_path')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    score = 0
    total_questions = questions.count()
    
    # Check answers
    for question in questions:
        answer_id = request.POST.get(f'question_{question.id}')
        if answer_id:
            answer = Answer.objects.filter(id=answer_id, is_correct=True).first()
            if answer:
                score += question.points
    
    # Calculate percentage
    max_score = sum(q.points for q in questions)
    percentage = int((score / max_score) * 100) if max_score > 0 else 0
    passed = percentage >= quiz.pass_percentage
    
    # Save attempt
    UserQuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        passed=passed
    )
    
    # If passed, complete the lesson
    if passed:
        user_lesson, created = UserLesson.objects.get_or_create(
            user=request.user,
            lesson=quiz.lesson
        )
        
        if not user_lesson.is_completed:
            user_lesson.is_completed = True
            user_lesson.completed_at = timezone.now()
            user_lesson.save()
            
            # Award points
            profile = request.user.profile
            profile.total_points += quiz.lesson.points
            profile.coins += quiz.lesson.coins
            profile.save()
            
            # Perfect score achievement
            if percentage == 100:
                check_perfect_score_achievement(request.user)
        
        messages.success(request, f'ممتاز! لقد نجحت في الاختبار بنسبة {percentage}%!')
    else:
        messages.warning(request, f'للأسف، لم تنجح في الاختبار. حصلت على {percentage}%. حاول مرة أخرى!')
    
    return redirect('lessons:learning_path')


@login_required
def generate_certificate(request, path_id):
    """Generate certificate for completed path"""
    path = get_object_or_404(LearningPath, id=path_id)
    
    # Check if all lessons are completed
    total_lessons = path.lessons.count()
    completed_lessons = UserLesson.objects.filter(
        user=request.user,
        lesson__path=path,
        is_completed=True
    ).count()
    
    if completed_lessons < total_lessons:
        messages.error(request, 'يجب إكمال جميع الدروس للحصول على الشهادة!')
        return redirect('lessons:learning_path')
    
    # Check if certificate already exists
    certificate = Certificate.objects.filter(
        user=request.user,
        path=path
    ).first()
    
    if not certificate:
        # Generate unique certificate number
        certificate_number = f"BVK-{timezone.now().year}-{request.user.id:04d}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
        
        certificate = Certificate.objects.create(
            user=request.user,
            path=path,
            certificate_number=certificate_number
        )
        
        messages.success(request, 'تهانينا! تم إصدار شهادتك بنجاح!')
    
    context = {
        'certificate': certificate,
    }
    
    return render(request, 'lessons/certificate.html', context)


def check_lesson_achievements(user):
    """Check and award lesson-related achievements"""
    completed_count = UserLesson.objects.filter(user=user, is_completed=True).count()
    
    # First lesson achievement
    if completed_count == 1:
        achievement = Achievement.objects.filter(
            achievement_type='lesson',
            points_required=1
        ).first()
        if achievement:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    
    # 5 lessons achievement
    elif completed_count == 5:
        achievement = Achievement.objects.filter(
            achievement_type='lesson',
            points_required=5
        ).first()
        if achievement:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    
    # 10 lessons achievement
    elif completed_count == 10:
        achievement = Achievement.objects.filter(
            achievement_type='lesson',
            points_required=10
        ).first()
        if achievement:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)


def check_perfect_score_achievement(user):
    """Award achievement for perfect quiz score"""
    achievement = Achievement.objects.filter(achievement_type='quiz').first()
    if achievement:
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)