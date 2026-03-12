from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from tasks.views import send_deadline_reminder

class Command(BaseCommand):
    help = 'Check for tasks with upcoming deadlines and send email reminders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Number of days before deadline to send reminder (default: 3)',
        )

    def handle(self, *args, **options):
        days_ahead = options['days']
        today = timezone.now().date()
        deadline_date = today + timedelta(days=days_ahead)
        
        # Find tasks with deadlines in the next X days that are not completed
        tasks = Task.objects.filter(
            due_date__lte=deadline_date,
            due_date__gte=today,
            status__in=['todo', 'in_progress']
        ).select_related('project', 'created_by').prefetch_related('assigned_to')
        
        sent_count = 0
        
        for task in tasks:
            self.stdout.write(f'Checking task: {task.title} (deadline: {task.due_date})')
            
            if send_deadline_reminder(task):
                sent_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Sent reminder for task: {task.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ No email addresses for task: {task.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal reminders sent: {sent_count}')
        )