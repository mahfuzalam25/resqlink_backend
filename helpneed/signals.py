from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import HelpPost, Notification

User = get_user_model()

@receiver(post_save, sender=HelpPost)
def notify_all_on_new_post(sender, instance: HelpPost, created, **kwargs):
    if not created:
        return
    # Create a notification for all users except the author
    users = User.objects.exclude(id=instance.author_id).only("id", "username")
    notifications = [
        Notification(
            user=u,
            actor=instance.author,
            post=instance,
            message=f"New help request: {instance.title} at {instance.location}",
        )
        for u in users
    ]
    if notifications:
        Notification.objects.bulk_create(notifications, ignore_conflicts=True)
