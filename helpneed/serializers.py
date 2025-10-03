from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import HelpPost, VolunteerResponse, Notification, VolunteerStat

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email",)

class HelpPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpPost
        fields = ("id", "title", "location", "exactLocation", "post_image", "work_description")

class VolunteerResponseSerializer(serializers.ModelSerializer):
    volunteer = UserMiniSerializer(read_only=True)

    class Meta:
        model = VolunteerResponse
        fields = ("id", "volunteer", "status", "responded_at")

class HelpPostListSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    responses = VolunteerResponseSerializer(many=True, read_only=True)

    class Meta:
        model = HelpPost
        fields = (
            "id", "author", "title", "location", "exactLocation",
            "post_image", "work_description", "is_completed", "created_at",
            "responders_count", "responses",
        )

class NotificationSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    actor = UserMiniSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "message", "created_at", "is_read", "post", "user", "actor")

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = VolunteerStat
        fields = ("user", "completed_count")
