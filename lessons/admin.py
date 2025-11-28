from django.contrib import admin
from .models import (
    LearningPath, Lesson, UserLesson, Quiz, Question, 
    Answer, UserQuizAttempt, Certificate
)

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'total_duration', 'is_active', 'order']
    list_filter = ['difficulty', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'path', 'order', 'duration', 'points', 'is_active']
    list_filter = ['path', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'progress_percentage', 'started_at']
    list_filter = ['is_completed', 'started_at']
    search_fields = ['user__username', 'lesson__title']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'pass_percentage', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'lesson__title']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text']
    inlines = [AnswerInline]


@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'percentage', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['completed_at']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'path', 'certificate_number', 'issued_at']
    list_filter = ['issued_at', 'path']
    search_fields = ['user__username', 'certificate_number']
    readonly_fields = ['issued_at']