from django.contrib import admin
from .models import HelpPost, VolunteerResponse, Notification, VolunteerStat

@admin.register(HelpPost)
class HelpPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "location", "is_completed", "responders_count", "created_at")
    search_fields = ("title", "location", "work_description", "author__username")
    list_filter = ("is_completed", "created_at")

@admin.register(VolunteerResponse)
class VolunteerResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "volunteer", "status", "responded_at")
    list_filter = ("status", "responded_at")
    search_fields = ("post__title", "volunteer__username")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "actor", "message", "post", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("message", "user__username", "actor__username", "post__title")

@admin.register(VolunteerStat)
class VolunteerStatAdmin(admin.ModelAdmin):
    list_display = ("user", "completed_count")
    search_fields = ("user__username",)
