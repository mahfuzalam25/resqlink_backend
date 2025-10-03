from django.contrib import admin
from .models import SafetyGuide, SafetyAdvice

# Register your models here.

admin.site.register(SafetyGuide)
admin.site.register(SafetyAdvice)