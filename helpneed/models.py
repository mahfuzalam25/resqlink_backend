from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os

def image_validator(value):
    ext = os.path.splitext(value.name)[1]
    validExtension = ['.jpg','.jpeg', '.png','.svg','.webp']
    if not ext.lower() in validExtension:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: .jpg, .jpeg, .png, .webp, .svg')


class HelpPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_posts")
    title = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=500)
    exactLocation = models.CharField(max_length=500, null=True, blank=True)

    post_image = models.FileField(upload_to="helpposts/", validators=[image_validator], null=True, blank=True)
    work_description = models.TextField()
    
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    responders_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"

class VolunteerResponse(models.Model):
    STATUS_CHOICES = [
        ("on_the_way", "On The Way"),
        ("completed", "Completed"),
    ]
    post = models.ForeignKey(HelpPost, on_delete=models.CASCADE, related_name="responses")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_responses")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="on_the_way")
    responded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "volunteer")

    def __str__(self):
        return f"{self.volunteer} -> {self.post} [{self.status}]"

class VolunteerStat(models.Model):
    """Keeps leaderboard data without touching users/models.py"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_stat")
    completed_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} completed: {self.completed_count}"

class Notification(models.Model):
    """Simple in-app notification model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # Optional references
    post = models.ForeignKey(HelpPost, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="actor_notifications")

    def __str__(self):
        return f"To {self.user}: {self.message}"
