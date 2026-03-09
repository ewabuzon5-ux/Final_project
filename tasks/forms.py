from django import forms
from .models import Project, Task, BudgetItem, Result

# Form for creating/editing projects
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 
            'description', 
            'status', 
            'start_date', 
            'end_date',
            'team_members',
            'total_budget',
            'grant_amount',
            'own_contribution_financial',
            'own_contribution_non_financial',
            'income_from_recipients',
        ]
        
        # Add Bootstrap classes to form fields
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa projektu'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Opis projektu',
                'rows': 4
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'team_members': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'total_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'grant_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'own_contribution_financial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'own_contribution_non_financial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'income_from_recipients': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }
        
        # Polish labels
        labels = {
            'name': 'Nazwa projektu',
            'description': 'Opis',
            'status': 'Status',
            'start_date': 'Data rozpoczęcia',
            'end_date': 'Data zakończenia',
            'team_members': 'Członkowie zespołu',
            'total_budget': 'Budżet całkowity (PLN)',
            'grant_amount': 'Dotacja (PLN)',
            'own_contribution_financial': 'Wkład własny finansowy (PLN)',
            'own_contribution_non_financial': 'Wkład własny niefinansowy (PLN)',
            'income_from_recipients': 'Przychody od odbiorców (PLN)',
        }
# Form for creating/editing tasks
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'cost',
            'project',
            'assigned_to',
        ]
        
        # Add Bootstrap classes to form fields
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tytuł zadania'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Opis zadania',
                'rows': 4
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
        }
        
        # Polish labels
        labels = {
            'title': 'Tytuł zadania',
            'description': 'Opis',
            'status': 'Status',
            'priority': 'Priorytet',
            'due_date': 'Termin wykonania',
            'cost': 'Koszt (PLN)',
            'project': 'Projekt',
            'assigned_to': 'Przypisane do',
        }
# Form for creating/editing budget items
class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = [
            'category',
            'cost_type',
            'unit_type',
            'unit_cost',
            'quantity',
            'year_1_amount',
            'year_2_amount',
            'year_3_amount',
        ]
        
        # Add Bootstrap classes to form fields
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'cost_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'np. Materiały szkoleniowe'
            }),
            'unit_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'np. godzina, sztuka, miesiąc'
            }),
            'unit_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'year_1_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'year_2_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'year_3_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
        
        # Polish labels
        labels = {
            'category': 'Kategoria',
            'cost_type': 'Rodzaj kosztu',
            'unit_type': 'Jednostka miary',
            'unit_cost': 'Koszt jednostkowy (PLN)',
            'quantity': 'Liczba jednostek',
            'year_1_amount': 'Rok 1 (PLN)',
            'year_2_amount': 'Rok 2 (PLN)',
            'year_3_amount': 'Rok 3 (PLN)',
        }
# Form for creating/editing results
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            'result_name',
            'target_value',
            'monitoring_method',
            'information_source',
            'status',
        ]
        
        # Add Bootstrap classes to form fields
        widgets = {
            'result_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'np. Liczba przeszkolonych osób'
            }),
            'target_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'np. 100 osób'
            }),
            'monitoring_method': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Opisz jak będzie monitorowany postęp',
                'rows': 3
            }),
            'information_source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'np. Listy obecności, ankiety ewaluacyjne'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
        # Polish labels
        labels = {
            'result_name': 'Nazwa rezultatu',
            'target_value': 'Planowany poziom osiągnięcia (wartość docelowa)',
            'monitoring_method': 'Sposób monitorowania rezultatów',
            'information_source': 'Źródło informacji o osiągnięciu wskaźnika',
            'status': 'Status realizacji',
        }