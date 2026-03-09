from rest_framework import serializers
from .models import Project, Task, BudgetItem, Result

class ProjectSerializer(serializers.ModelSerializer):
    coordinator_name = serializers.CharField(source='coordinator.username', read_only=True)
    completion_percentage = serializers.SerializerMethodField()
    budget_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 
            'start_date', 'end_date', 
            'coordinator', 'coordinator_name',
            'total_budget', 'grant_amount',
            'completion_percentage', 'budget_percentage',
            'created_at'
        ]
    
    def get_completion_percentage(self, obj):
        return round(obj.get_completion_percentage(), 2)
    
    def get_budget_percentage(self, obj):
        return round(obj.get_budget_percentage(), 2)


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_to_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'cost', 
            'project', 'project_name',
            'assigned_to', 'assigned_to_names',
            'created_at'
        ]
    
    def get_assigned_to_names(self, obj):
        return [user.username for user in obj.assigned_to.all()]


class BudgetItemSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = BudgetItem
        fields = [
            'id', 'project', 'project_name', 'category',
            'cost_type', 'unit_type', 'unit_cost', 'quantity',
            'year_1_amount', 'year_2_amount', 'year_3_amount',
            'total_value'
        ]


class ResultSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Result
        fields = [
            'id', 'project', 'project_name',
            'result_name', 'target_value', 
            'monitoring_method', 'information_source',
            'status'
        ]