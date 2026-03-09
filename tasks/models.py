from django.db import models
from django.contrib.auth.models import User

# Extended User Profile to store role information
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('coordinator', 'Coordinator'),
        ('executor', 'Executor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='executor')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Project Model
class Project(models.Model):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    # Basic information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Team
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coordinated_projects')
    team_members = models.ManyToManyField(User, related_name='assigned_projects', blank=True)
    
    # Budget - sources of financing
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grant_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    own_contribution_financial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    own_contribution_non_financial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_from_recipients = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projekt"
        verbose_name_plural = "Projekty"
    
    def __str__(self):
        return self.name
    
    # Calculate total spent from all budget items
    def get_total_spent(self):
        return sum(item.total_value for item in self.budget_items.all())
    
    # Calculate percentage of budget used
    def get_budget_percentage(self):
        if self.total_budget > 0:
            return (self.get_total_spent() / self.total_budget) * 100
        return 0
    
    # Calculate percentage of completed tasks
    def get_completion_percentage(self):
        total_tasks = self.tasks.count()
        if total_tasks > 0:
            completed_tasks = self.tasks.filter(status='completed').count()
            return (completed_tasks / total_tasks) * 100
        return 0


# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Dates
    due_date = models.DateField(null=True, blank=True)
    
    # Cost
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Relations
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"
    
    def __str__(self):
        return self.title


# Budget Item Model - detailed cost breakdown
class BudgetItem(models.Model):
    CATEGORY_CHOICES = [
        ('implementation', 'Implementation Costs'),
        ('administrative', 'Administrative Costs'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budget_items')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Cost details
    cost_type = models.CharField(max_length=200)  # e.g., "Training materials"
    unit_type = models.CharField(max_length=50)   # e.g., "hour", "piece", "month"
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Multi-year breakdown
    year_1_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    year_2_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    year_3_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Total value (calculated automatically)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pozycja budżetowa"
        verbose_name_plural = "Pozycje budżetowe"
    
    def __str__(self):
        return f"{self.cost_type} - {self.project.name}"
    
    # Auto-calculate total value before saving
    def save(self, *args, **kwargs):
        self.total_value = self.unit_cost * self.quantity
        super().save(*args, **kwargs)


# Result Model - project outcomes/goals
class Result(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('achieved', 'Achieved'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='results')
    
    result_name = models.CharField(max_length=200)
    target_value = models.CharField(max_length=100)  # Can be number or description
    monitoring_method = models.TextField()
    information_source = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rezultat"
        verbose_name_plural = "Rezultaty"
    
    def __str__(self):
        return f"{self.result_name} - {self.project.name}"


# Extended User Profile to store role information
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('coordinator', 'Coordinator'),
        ('executor', 'Executor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='executor')
    
    class Meta:
        verbose_name = "Profil użytkownika"
        verbose_name_plural = "Profile użytkowników"
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"