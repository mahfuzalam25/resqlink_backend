from django.db import models
import os
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
import os
from datetime import timedelta
from django.utils import timezone
# Create your models here.

def image_validator(value):
    ext = os.path.splitext(value.name)[1]
    validExtension = ['.jpg','.jpeg', '.png','.svg','.webp']
    if not ext.lower() in validExtension:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: .jpg, .jpeg, .png, .webp, .svg')


@deconstructible
class GenerateProfileImagePath(object):
    def __init__(self):
        pass

    def __call_(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images/'
        name = f'profile_image.{ext}'
        return os.path.join(path,name)

class Location(models.Model):
    home_address = models.CharField(max_length=255, blank=True, null=True)
    office_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    division = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.city or 'Unknown'}, {self.district or ''}, {self.division or ''}"



class Experience(models.Model):
    experience_title = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)  # e.g. "Sep 2022 - Present"
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    organization_address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.experience_title or 'No title'



class Education(models.Model):
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)  # e.g. "Sep 2022 - Present"
    department_name = models.CharField(max_length=255, blank=True, null=True)
    institution_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.institution_name or 'No institution'



class Certification(models.Model):
    certificate_title = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)  # e.g. "2023"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.certificate_title or 'No certificate'



user_profile_image_path = GenerateProfileImagePath()
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.FileField(upload_to='profile/', validators=[image_validator], null=True, blank=True)
    bio = models.CharField(max_length=150, blank=True)
    blood_group = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True)
    experience = models.OneToOneField(Experience, on_delete=models.CASCADE, null=True, blank=True)
    education = models.OneToOneField(Education, on_delete=models.CASCADE, null=True, blank=True)
    certification = models.OneToOneField(Certification, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.user.username}\'s Profile'
    


class SignupOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - Signup OTP"

    
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - {self.code}"
