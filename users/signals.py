from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile, Location, Experience, Education, Certification

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create related objects
        location = Location.objects.create()
        experience = Experience.objects.create()
        education = Education.objects.create()
        certification = Certification.objects.create()

        # Create the profile and link the related objects
        Profile.objects.create(
            user=instance,
            location=location,
            experience=experience,
            education=education,
            certification=certification
        )


@receiver(post_delete, sender=Profile)
def delete_related_models(sender, instance, **kwargs):
    for field_name in ['location', 'experience', 'education', 'certification']:
        related_obj = getattr(instance, field_name, None)
        if related_obj:
            related_obj.delete()

@receiver (pre_save, sender = User)
def set_username(sender, instance,**kwargs):
    if not instance.username:
        username = f'{instance.first_name}'.lower()
        counter = 1
        while User.objects.filter(username=username):
            username = f'{instance.first_name}_{counter}'.lower()
            counter += 1
        instance.username = username