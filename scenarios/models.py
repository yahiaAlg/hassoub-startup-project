from django.db import models
from django.contrib.auth.models import User

class Scenario(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    CATEGORY_CHOICES = [
        ('lemonade', 'Lemonade Stand'),
        ('toy_shop', 'Toy Shop'),
        ('restaurant', 'Restaurant'),
        ('bakery', 'Bakery'),
        ('farm', 'Farm'),
        ('tech', 'Tech Startup'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    initial_budget = models.DecimalField(max_digits=10, decimal_places=2)
    target_profit = models.DecimalField(max_digits=10, decimal_places=2)
    time_limit = models.IntegerField(help_text='Time limit in minutes')
    points_reward = models.IntegerField(default=50)
    coins_reward = models.IntegerField(default=25)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title


class Product(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)
    suggested_price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.scenario.title} - {self.name}"


class ScenarioEvent(models.Model):
    EVENT_TYPES = [
        ('weather', 'Weather'),
        ('customer', 'Customer'),
        ('market', 'Market'),
        ('special', 'Special'),
    ]
    
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    impact_text = models.CharField(max_length=200)
    probability = models.IntegerField(default=20, help_text='Probability percentage')
    
    def __str__(self):
        return f"{self.scenario.title} - {self.title}"


class UserScenario(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_scenarios')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='user_attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    current_budget = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    days_played = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.scenario.title}"
    
    def calculate_profit(self):
        return self.total_revenue - self.total_costs


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('expense', 'Expense'),
    ]
    
    user_scenario = models.ForeignKey(UserScenario, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=200)
    day = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['day', '-created_at']
        
    def __str__(self):
        return f"{self.user_scenario} - {self.transaction_type} - {self.amount}"


class Inventory(models.Model):
    user_scenario = models.ForeignKey(UserScenario, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user_scenario', 'product']
        
    def __str__(self):
        return f"{self.user_scenario} - {self.product.name}: {self.quantity}"