from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('progress-rewards/', views.progress_rewards, name='progress_rewards'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/add-child/', views.add_child, name='add_child'),
    path('parent/remove-child/<int:child_id>/', views.remove_child, name='remove_child'),
]