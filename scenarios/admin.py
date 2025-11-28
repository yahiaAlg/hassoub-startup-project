from django.contrib import admin
from .models import Scenario, Product, ScenarioEvent, UserScenario, Transaction, Inventory

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'initial_budget', 'target_profit', 'is_active']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'scenario', 'base_cost', 'suggested_price']
    list_filter = ['scenario']
    search_fields = ['name', 'scenario__title']


@admin.register(ScenarioEvent)
class ScenarioEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'scenario', 'event_type', 'probability']
    list_filter = ['event_type', 'scenario']
    search_fields = ['title', 'description']


@admin.register(UserScenario)
class UserScenarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario', 'status', 'final_profit', 'days_played', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['user__username', 'scenario__title']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user_scenario', 'transaction_type', 'product', 'amount', 'quantity', 'day']
    list_filter = ['transaction_type', 'day']
    search_fields = ['user_scenario__user__username', 'description']
    readonly_fields = ['created_at']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['user_scenario', 'product', 'quantity']
    list_filter = ['product']
    search_fields = ['user_scenario__user__username', 'product__name']