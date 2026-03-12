from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Task, BudgetItem, Result, UserProfile
from .forms import ProjectForm, TaskForm, BudgetItemForm, ResultForm, UserRegistrationForm
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializer, TaskSerializer, BudgetItemSerializer, ResultSerializer

# Dashboard - main page after login
@login_required
def dashboard(request):
    # Get user's projects based on role
    if request.user.profile.role == 'coordinator':
        # Coordinator sees all their coordinated projects
        projects = Project.objects.filter(coordinator=request.user)
    else:
        # Executor sees projects they're assigned to
        projects = request.user.assigned_projects.all()
    
    # Calculate statistics
    total_projects = projects.count()
    completed_projects = projects.filter(status='completed').count()
    in_progress_projects = projects.filter(status='in_progress').count()
    
    # Get user's tasks
    my_tasks = Task.objects.filter(assigned_to=request.user).count()
    
    # Get 5 most recent projects
    recent_projects = projects.order_by('-created_at')[:5]
    
    context = {
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'in_progress_projects': in_progress_projects,
        'my_tasks': my_tasks,
        'recent_projects': recent_projects,
    }
    
    return render(request, 'tasks/dashboard.html', context)


# List all projects
@login_required
def project_list(request):
    # Get projects based on user role
    if request.user.profile.role == 'coordinator':
        projects = Project.objects.filter(coordinator=request.user)
    else:
        projects = request.user.assigned_projects.all()
    
    context = {
        'projects': projects,
    }
    
    return render(request, 'tasks/project_list.html', context)


# Project details
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user has access to this project
    if request.user.profile.role == 'coordinator':
        # Coordinator can only see their own projects
        if project.coordinator != request.user:
            messages.error(request, 'Nie masz dostępu do tego projektu.')
            return redirect('project_list')
    else:
        # Executor can only see projects they're assigned to
        if request.user not in project.team_members.all():
            messages.error(request, 'Nie masz dostępu do tego projektu.')
            return redirect('project_list')
    
    context = {
        'project': project,
    }
    
    return render(request, 'tasks/project_detail.html', context)

# Create new project (only for coordinators)
@login_required
def project_create(request):
    # Check if user is coordinator
    if request.user.profile.role != 'coordinator':
        messages.error(request, 'Tylko koordynatorzy mogą tworzyć projekty.')
        return redirect('project_list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.coordinator = request.user  # Set current user as coordinator
            project.save()
            form.save_m2m()  # Save many-to-many relationships (team_members)
            messages.success(request, f'Projekt "{project.name}" został utworzony!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'title': 'Nowy projekt',
    }
    
    return render(request, 'tasks/project_form.html', context)


# Edit existing project (only for coordinators)
@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is the coordinator of this project
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może go edytować.')
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Projekt "{project.name}" został zaktualizowany!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'title': 'Edytuj projekt',
    }
    
    return render(request, 'tasks/project_form.html', context)


# Delete project (only for coordinators)
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is the coordinator of this project
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może go usunąć.')
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'Projekt "{project_name}" został usunięty.')
        return redirect('project_list')
    
    context = {
        'project': project,
    }
    
    return render(request, 'tasks/project_confirm_delete.html', context)
# Create new task
@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    # Check if user has access to this project
    if request.user.profile.role == 'coordinator':
        if project.coordinator != request.user:
            messages.error(request, 'Nie masz dostępu do tego projektu.')
            return redirect('project_list')
    else:
        if request.user not in project.team_members.all():
            messages.error(request, 'Nie masz dostępu do tego projektu.')
            return redirect('project_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'Zadanie "{task.title}" zostało utworzone!')
            return redirect('project_detail', pk=project.pk)
    else:
        # Pre-fill project field
        form = TaskForm(initial={'project': project})
    
    context = {
        'form': form,
        'project': project,
        'title': 'Nowe zadanie',
    }
    
    return render(request, 'tasks/task_form.html', context)


# Edit existing task
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    
    # Check permissions
    if request.user.profile.role == 'coordinator':
        if project.coordinator != request.user:
            messages.error(request, 'Nie masz uprawnień do edycji tego zadania.')
            return redirect('project_detail', pk=project.pk)
    else:
        # Executor can only edit tasks assigned to them
        if request.user not in task.assigned_to.all():
            messages.error(request, 'Możesz edytować tylko zadania przypisane do Ciebie.')
            return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zadanie "{task.title}" zostało zaktualizowane!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'project': project,
        'title': 'Edytuj zadanie',
    }
    
    return render(request, 'tasks/task_form.html', context)


# Delete task
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    
    # Only coordinator can delete tasks
    if request.user.profile.role != 'coordinator' or project.coordinator != request.user:
        messages.error(request, 'Tylko koordynator projektu może usuwać zadania.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Zadanie "{task_title}" zostało usunięte.')
        return redirect('project_detail', pk=project.pk)
    
    context = {
        'task': task,
        'project': project,
    }
    
    return render(request, 'tasks/task_confirm_delete.html', context)
# Create new budget item
@login_required
def budget_item_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    # Only coordinator can add budget items
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może dodawać pozycje budżetowe.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = BudgetItemForm(request.POST)
        if form.is_valid():
            budget_item = form.save(commit=False)
            budget_item.project = project
            budget_item.save()
            messages.success(request, 'Pozycja budżetowa została dodana!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = BudgetItemForm()
    
    context = {
        'form': form,
        'project': project,
        'title': 'Nowa pozycja budżetowa',
    }
    
    return render(request, 'tasks/budget_item_form.html', context)


# Edit budget item
@login_required
def budget_item_edit(request, pk):
    budget_item = get_object_or_404(BudgetItem, pk=pk)
    project = budget_item.project
    
    # Only coordinator can edit budget items
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może edytować pozycje budżetowe.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = BudgetItemForm(request.POST, instance=budget_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pozycja budżetowa została zaktualizowana!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = BudgetItemForm(instance=budget_item)
    
    context = {
        'form': form,
        'budget_item': budget_item,
        'project': project,
        'title': 'Edytuj pozycję budżetową',
    }
    
    return render(request, 'tasks/budget_item_form.html', context)


# Delete budget item
@login_required
def budget_item_delete(request, pk):
    budget_item = get_object_or_404(BudgetItem, pk=pk)
    project = budget_item.project
    
    # Only coordinator can delete budget items
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może usuwać pozycje budżetowe.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        budget_item.delete()
        messages.success(request, 'Pozycja budżetowa została usunięta.')
        return redirect('project_detail', pk=project.pk)
    
    context = {
        'budget_item': budget_item,
        'project': project,
    }
    
    return render(request, 'tasks/budget_item_confirm_delete.html', context)
# Create new result
@login_required
def result_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    # Only coordinator can add results
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może dodawać rezultaty.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.project = project
            result.save()
            messages.success(request, 'Rezultat został dodany!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ResultForm()
    
    context = {
        'form': form,
        'project': project,
        'title': 'Nowy rezultat',
    }
    
    return render(request, 'tasks/result_form.html', context)


# Edit result
@login_required
def result_edit(request, pk):
    result = get_object_or_404(Result, pk=pk)
    project = result.project
    
    # Only coordinator can edit results
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może edytować rezultaty.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rezultat został zaktualizowany!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ResultForm(instance=result)
    
    context = {
        'form': form,
        'result': result,
        'project': project,
        'title': 'Edytuj rezultat',
    }
    
    return render(request, 'tasks/result_form.html', context)


# Delete result
@login_required
def result_delete(request, pk):
    result = get_object_or_404(Result, pk=pk)
    project = result.project
    
    # Only coordinator can delete results
    if request.user != project.coordinator:
        messages.error(request, 'Tylko koordynator projektu może usuwać rezultaty.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Rezultat został usunięty.')
        return redirect('project_detail', pk=project.pk)
    
    context = {
        'result': result,
        'project': project,
    }
    
    return render(request, 'tasks/result_confirm_delete.html', context)
# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            # Create UserProfile with selected role
            role = form.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
            
            # Log the user in
            from django.contrib.auth import login
            login(request, user)
            
            messages.success(request, f'Witaj {user.username}! Twoje konto zostało utworzone.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'tasks/register.html', context)

# ========== REST API VIEWS ==========
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializer, TaskSerializer, BudgetItemSerializer, ResultSerializer

class IsCoordinatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Coordinators can edit, others can only read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for coordinator
        if hasattr(obj, 'coordinator'):
            return obj.coordinator == request.user
        elif hasattr(obj, 'project'):
            return obj.project.coordinator == request.user
        
        return False


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for projects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordinatorOrReadOnly]
    
    def get_queryset(self):
        # Users only see their own projects
        user = self.request.user
        if user.profile.role == 'coordinator':
            return Project.objects.filter(coordinator=user)
        else:
            return user.assigned_projects.all()


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tasks
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter tasks by user's projects
        user = self.request.user
        if user.profile.role == 'coordinator':
            return Task.objects.filter(project__coordinator=user)
        else:
            return Task.objects.filter(assigned_to=user)


class BudgetItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for budget items
    """
    queryset = BudgetItem.objects.all()
    serializer_class = BudgetItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordinatorOrReadOnly]


class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for results
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordinatorOrReadOnly]