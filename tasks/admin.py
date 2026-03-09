from django.contrib import admin
from .models import UserProfile, Project, Task, BudgetItem, Result

# Register UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']

# Register Project with more details
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'coordinator', 'status', 'start_date', 'end_date', 'total_budget']
    list_filter = ['status', 'start_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['team_members']  # Nice widget for many-to-many

# Register Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'due_date', 'cost']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    filter_horizontal = ['assigned_to']

# Register BudgetItem
@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ['cost_type', 'project', 'category', 'unit_cost', 'quantity', 'total_value']
    list_filter = ['category', 'project']
    search_fields = ['cost_type']

# Register Result
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['result_name', 'project', 'target_value', 'status']
    list_filter = ['status', 'project']
    search_fields = ['result_name']