from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from .models import Scenario, Product, UserScenario, Transaction, Inventory
import random


@login_required
def scenario_list(request):
    """Display all available scenarios"""
    scenarios = Scenario.objects.filter(is_active=True)

    # Get user's completed scenarios
    completed_scenarios = UserScenario.objects.filter(
        user=request.user, status="completed"
    ).values_list("scenario_id", flat=True)

    scenarios_data = []
    for scenario in scenarios:
        user_attempts = UserScenario.objects.filter(
            user=request.user, scenario=scenario
        ).count()

        best_score = (
            UserScenario.objects.filter(
                user=request.user, scenario=scenario, status="completed"
            ).aggregate(best=Sum("final_profit"))["best"]
            or 0
        )

        scenarios_data.append(
            {
                "scenario": scenario,
                "is_completed": scenario.id in completed_scenarios,
                "attempts": user_attempts,
                "best_score": best_score,
            }
        )

    context = {
        "scenarios_data": scenarios_data,
    }

    return render(request, "scenarios/scenario_list.html", context)


@login_required
def scenario_start(request, scenario_id):
    """Start a new scenario"""
    scenario = get_object_or_404(Scenario, id=scenario_id, is_active=True)

    if request.method == "POST":
        # Create new user scenario
        user_scenario = UserScenario.objects.create(
            user=request.user,
            scenario=scenario,
            current_budget=scenario.initial_budget,
            status="in_progress",
        )

        # Initialize inventory
        products = scenario.products.all()
        for product in products:
            Inventory.objects.create(
                user_scenario=user_scenario, product=product, quantity=0
            )

        messages.success(request, f'بدأت سيناريو "{scenario.title}"!')
        return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)

    # Get products for this scenario
    products = scenario.products.all()

    context = {
        "scenario": scenario,
        "products": products,
    }

    return render(request, "scenarios/scenario_start.html", context)


@login_required
def scenario_play(request, user_scenario_id):
    """Main gameplay view"""
    user_scenario = get_object_or_404(
        UserScenario, id=user_scenario_id, user=request.user
    )

    if user_scenario.status != "in_progress":
        messages.warning(request, "هذا السيناريو قد انتهى بالفعل!")
        return redirect("scenarios:scenario_result", user_scenario_id=user_scenario.id)

    scenario = user_scenario.scenario
    inventory = user_scenario.inventory.select_related("product")
    products = scenario.products.all()

    # Get recent transactions
    recent_transactions = user_scenario.transactions.all()[:10]

    # Calculate current profit
    current_profit = user_scenario.total_revenue - user_scenario.total_costs

    context = {
        "user_scenario": user_scenario,
        "scenario": scenario,
        "inventory": inventory,
        "products": products,
        "recent_transactions": recent_transactions,
        "current_profit": current_profit,
    }

    return render(request, "scenarios/scenario_play.html", context)


@login_required
def buy_product(request, user_scenario_id):
    """Buy product (add to inventory)"""
    if request.method != "POST":
        return redirect("scenarios:scenario_list")

    user_scenario = get_object_or_404(
        UserScenario, id=user_scenario_id, user=request.user
    )

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))

    if quantity <= 0:
        messages.error(request, "الكمية يجب أن تكون أكبر من صفر!")
        return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)

    product = get_object_or_404(Product, id=product_id, scenario=user_scenario.scenario)

    total_cost = product.base_cost * quantity

    # Check if user has enough budget
    if user_scenario.current_budget < total_cost:
        messages.error(request, "ليس لديك ميزانية كافية!")
        return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)

    # Update budget
    user_scenario.current_budget -= total_cost
    user_scenario.total_costs += total_cost
    user_scenario.save()

    # Update inventory
    inventory_item = Inventory.objects.get(user_scenario=user_scenario, product=product)
    inventory_item.quantity += quantity
    inventory_item.save()

    # Record transaction
    Transaction.objects.create(
        user_scenario=user_scenario,
        transaction_type="purchase",
        product=product,
        amount=total_cost,
        quantity=quantity,
        description=f"شراء {quantity} {product.name}",
        day=user_scenario.days_played,
    )

    messages.success(request, f"تم شراء {quantity} {product.name} بنجاح!")
    return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)


@login_required
def sell_product(request, user_scenario_id):
    """Sell product to customers"""
    if request.method != "POST":
        return redirect("scenarios:scenario_list")

    user_scenario = get_object_or_404(
        UserScenario, id=user_scenario_id, user=request.user
    )

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))
    price = Decimal(request.POST.get("price", 0))

    if quantity <= 0 or price <= 0:
        messages.error(request, "الكمية والسعر يجب أن يكونا أكبر من صفر!")
        return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)

    product = get_object_or_404(Product, id=product_id)

    # Check inventory
    inventory_item = Inventory.objects.get(user_scenario=user_scenario, product=product)

    if inventory_item.quantity < quantity:
        messages.error(request, "ليس لديك مخزون كافٍ!")
        return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)

    # Calculate actual sales (random customer interest)
    demand_multiplier = 1.0

    # Price sensitivity
    if price > product.suggested_price * Decimal("1.2"):
        demand_multiplier = 0.5  # High price, low demand
    elif price < product.suggested_price * Decimal("0.8"):
        demand_multiplier = 1.5  # Low price, high demand

    actual_quantity = int(quantity * demand_multiplier * random.uniform(0.6, 1.0))
    actual_quantity = min(actual_quantity, inventory_item.quantity)

    if actual_quantity == 0:
        messages.warning(request, "لم يتم بيع أي منتجات! قد يكون السعر مرتفعاً جداً.")
        return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)

    total_revenue = price * actual_quantity

    # Update budget and revenue
    user_scenario.current_budget += total_revenue
    user_scenario.total_revenue += total_revenue
    user_scenario.save()

    # Update inventory
    inventory_item.quantity -= actual_quantity
    inventory_item.save()

    # Record transaction
    Transaction.objects.create(
        user_scenario=user_scenario,
        transaction_type="sale",
        product=product,
        amount=total_revenue,
        quantity=actual_quantity,
        description=f"بيع {actual_quantity} {product.name} بسعر {price}",
        day=user_scenario.days_played,
    )

    messages.success(request, f"تم بيع {actual_quantity} {product.name} بنجاح!")
    return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)


@login_required
def next_day(request, user_scenario_id):
    """Advance to next day in scenario"""
    if request.method != "POST":
        return redirect("scenarios:scenario_list")

    user_scenario = get_object_or_404(
        UserScenario, id=user_scenario_id, user=request.user
    )

    # Increment day
    user_scenario.days_played += 1

    # Random expenses (rent, utilities, etc.)
    daily_expense = Decimal(random.randint(10, 50))
    user_scenario.current_budget -= daily_expense
    user_scenario.total_costs += daily_expense

    # Record expense
    Transaction.objects.create(
        user_scenario=user_scenario,
        transaction_type="expense",
        amount=daily_expense,
        quantity=1,
        description="تكاليف يومية (إيجار، كهرباء، إلخ)",
        day=user_scenario.days_played,
    )

    # Random event
    events = user_scenario.scenario.events.all()
    if events and random.randint(1, 100) <= 30:  # 30% chance of event
        event = random.choice(events)
        messages.info(request, f"حدث: {event.title} - {event.description}")

    user_scenario.save()

    messages.success(request, f"اليوم {user_scenario.days_played} بدأ!")
    return redirect("scenarios:scenario_play", user_scenario_id=user_scenario.id)


@login_required
def end_scenario(request, user_scenario_id):
    """End the scenario and calculate final results"""
    if request.method != "POST":
        return redirect("scenarios:scenario_list")

    user_scenario = get_object_or_404(
        UserScenario, id=user_scenario_id, user=request.user
    )

    # Calculate final profit
    final_profit = user_scenario.total_revenue - user_scenario.total_costs
    user_scenario.final_profit = final_profit

    # Determine success
    if final_profit >= user_scenario.scenario.target_profit:
        user_scenario.status = "completed"

        # Award points and coins
        profile = request.user.profile
        profile.total_points += user_scenario.scenario.points_reward
        profile.coins += user_scenario.scenario.coins_reward
        profile.save()

        messages.success(
            request,
            f"مبروك! لقد حققت الهدف وحصلت على {user_scenario.scenario.points_reward} نقطة!",
        )
    else:
        user_scenario.status = "failed"
        messages.info(request, "للأسف، لم تحقق الهدف المطلوب. حاول مرة أخرى!")

    user_scenario.completed_at = timezone.now()
    user_scenario.save()

    return redirect("scenarios:scenario_result", user_scenario_id=user_scenario.id)


@login_required
def scenario_result(request, user_scenario_id):
    """Display scenario results"""
    user_scenario = get_object_or_404(
        UserScenario, id=user_scenario_id, user=request.user
    )

    # Get all transactions
    transactions = user_scenario.transactions.all()

    # Calculate statistics
    total_sales = (
        transactions.filter(transaction_type="sale").aggregate(total=Sum("amount"))[
            "total"
        ]
        or 0
    )

    total_purchases = (
        transactions.filter(transaction_type="purchase").aggregate(total=Sum("amount"))[
            "total"
        ]
        or 0
    )

    total_expenses = (
        transactions.filter(transaction_type="expense").aggregate(total=Sum("amount"))[
            "total"
        ]
        or 0
    )

    context = {
        "user_scenario": user_scenario,
        "transactions": transactions,
        "total_sales": total_sales,
        "total_purchases": total_purchases,
        "total_expenses": total_expenses,
        "success": user_scenario.status == "completed",
    }

    return render(request, "scenarios/scenario_result.html", context)
