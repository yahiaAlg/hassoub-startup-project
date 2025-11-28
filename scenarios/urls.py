from django.urls import path
from . import views

app_name = 'scenarios'

urlpatterns = [
    path('', views.scenario_list, name='scenario_list'),
    path('<int:scenario_id>/start/', views.scenario_start, name='scenario_start'),
    path('play/<int:user_scenario_id>/', views.scenario_play, name='scenario_play'),
    path('play/<int:user_scenario_id>/buy/', views.buy_product, name='buy_product'),
    path('play/<int:user_scenario_id>/sell/', views.sell_product, name='sell_product'),
    path('play/<int:user_scenario_id>/next-day/', views.next_day, name='next_day'),
    path('play/<int:user_scenario_id>/end/', views.end_scenario, name='end_scenario'),
    path('result/<int:user_scenario_id>/', views.scenario_result, name='scenario_result'),
]