from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Task

# Automatically create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create UserProfile automatically when new User is created
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save UserProfile when User is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Email notification when new task is created
@receiver(post_save, sender=Task)
def notify_new_task(sender, instance, created, **kwargs):
    """
    Send email notification to project coordinator when new task is created
    """
    if created:  # Only for new tasks, not updates
        from tasks.views import send_new_task_notification
        try:
            send_new_task_notification(instance)
        except Exception as e:
            # Don't break task creation if email fails
            print(f"Failed to send email notification: {e}")