from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Scenario, UserScenario


def scenario_list(request):
    """Display all available scenarios (games.html)"""
    scenarios = Scenario.objects.filter(is_active=True)

    context = {
        "scenarios": scenarios,
    }

    return render(request, "scenarios/games.html", context)


def scenario_detail(request, slug):
    """Display and play a specific scenario"""
    scenario = get_object_or_404(Scenario, slug=slug, is_active=True)

    # Get or create user scenario if authenticated
    user_scenario = None
    if request.user.is_authenticated:
        user_scenario, created = UserScenario.objects.get_or_create(
            user=request.user, scenario=scenario, defaults={"status": "in_progress"}
        )

    context = {
        "scenario": scenario,
        "user_scenario": user_scenario,
    }

    # Render the specific scenario template
    template_name = f"scenarios/{slug}.html"
    return render(request, template_name, context)


@login_required
def complete_scenario(request, slug):
    """Mark scenario as completed"""
    if request.method != "POST":
        return redirect("scenarios:scenario_list")

    scenario = get_object_or_404(Scenario, slug=slug)
    score = int(request.POST.get("score", 0))

    # Update or create user scenario
    user_scenario, created = UserScenario.objects.get_or_create(
        user=request.user,
        scenario=scenario,
        defaults={"status": "completed", "score": score},
    )

    if not created:
        user_scenario.status = "completed"
        user_scenario.score = max(user_scenario.score, score)
        user_scenario.save()

    # Award points and coins to user profile
    profile = request.user.profile
    profile.total_points += scenario.points_reward
    profile.coins += scenario.coins_reward
    profile.save()

    messages.success(
        request,
        f'مبروك! لقد أكملت "{scenario.title}" وحصلت على {scenario.points_reward} نقطة و{scenario.coins_reward} عملة!',
    )

    return redirect("scenarios:scenario_list")
