from django.db import models
from django.contrib.auth.models import User

class LearningPath(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='💰')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    min_age = models.IntegerField(default=10)
    max_age = models.IntegerField(default=14)
    total_duration = models.IntegerField(help_text='Total duration in minutes')
    certificate_available = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title
    
    def get_total_lessons(self):
        return self.lessons.count()
    
    def get_completion_percentage(self, user):
        total = self.lessons.count()
        if total == 0:
            return 0
        completed = UserLesson.objects.filter(
            user=user,
            lesson__path=self,
            is_completed=True
        ).count()
        return int((completed / total) * 100)


class Lesson(models.Model):
    STATUS_CHOICES = [
        ('locked', 'Locked'),
        ('unlocked', 'Unlocked'),
        ('completed', 'Completed'),
    ]
    
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10)
    duration = models.IntegerField(help_text='Duration in minutes')
    order = models.IntegerField(default=0)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    points = models.IntegerField(default=10)
    coins = models.IntegerField(default=5)
    requires_previous = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['path', 'order']
        unique_together = ['path', 'order']
        
    def __str__(self):
        return f"{self.path.title} - {self.title}"
    
    def is_locked_for_user(self, user):
        """Check if lesson is locked for a specific user"""
        if not self.requires_previous or self.order == 1:
            return False
        
        # Check if previous lesson is completed
        previous_lesson = Lesson.objects.filter(
            path=self.path,
            order=self.order - 1
        ).first()
        
        if previous_lesson:
            user_lesson = UserLesson.objects.filter(
                user=user,
                lesson=previous_lesson,
                is_completed=True
            ).exists()
            return not user_lesson
        
        return False


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    progress_percentage = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.IntegerField(default=0, help_text='Time spent in minutes')
    
    class Meta:
        unique_together = ['user', 'lesson']
        ordering = ['-started_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pass_percentage = models.IntegerField(default=70)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('text', 'Text Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple')
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    explanation = models.TextField(blank=True)
    
    class Meta:
        ordering = ['quiz', 'order']
        
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['question', 'order']
        
    def __str__(self):
        return f"{self.question} - {self.answer_text[:50]}"


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.percentage}%"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'path']
        ordering = ['-issued_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.path.title} Certificate"