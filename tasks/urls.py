from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# REST API Router
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='api-project')
router.register(r'tasks', views.TaskViewSet, basename='api-task')
router.register(r'budget-items', views.BudgetItemViewSet, basename='api-budgetitem')
router.register(r'results', views.ResultViewSet, basename='api-result')

urlpatterns = [
    # Web interface URLs
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Task URLs
    path('projects/<int:project_pk>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    
    # Budget Item URLs
    path('projects/<int:project_pk>/budget/create/', views.budget_item_create, name='budget_item_create'),
    path('budget/<int:pk>/edit/', views.budget_item_edit, name='budget_item_edit'),
    path('budget/<int:pk>/delete/', views.budget_item_delete, name='budget_item_delete'),
    
    # Result URLs
    path('projects/<int:project_pk>/results/create/', views.result_create, name='result_create'),
    path('results/<int:pk>/edit/', views.result_edit, name='result_edit'),
    path('results/<int:pk>/delete/', views.result_delete, name='result_delete'),
    
    # REST API URLs
    path('api/', include(router.urls)),
]