from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.learning_path, name='learning_path'),
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('certificate/<int:path_id>/', views.generate_certificate, name='generate_certificate'),
]