from django.urls import path
from . import views

app_name = "scenarios"

urlpatterns = [
    path("", views.scenario_list, name="scenario_list"),
    path("<slug:slug>/", views.scenario_detail, name="scenario_detail"),
    path("<slug:slug>/complete/", views.complete_scenario, name="complete_scenario"),
]
