from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import HelpPost, VolunteerResponse, Notification, VolunteerStat
from .serializers import (
    HelpPostCreateSerializer, HelpPostListSerializer,
    VolunteerResponseSerializer, NotificationSerializer, LeaderboardEntrySerializer
)
from .permissions import IsAuthorOrReadOnly

User = get_user_model()

class HelpPostViewSet(viewsets.ModelViewSet):
    queryset = HelpPost.objects.select_related("author").prefetch_related("responses__volunteer").order_by("-created_at")
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return HelpPostCreateSerializer
        return HelpPostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def respond(self, request, pk=None):
        """
        Volunteer taps 'On the way' -> creates (or returns) a VolunteerResponse.
        Notifies the post author.
        """
        post = self.get_object()
        if post.is_completed:
            return Response({"detail": "This task is already completed."}, status=400)

        # prevent author from responding to own post
        if post.author_id == request.user.id:
            return Response({"detail": "Authors cannot respond to their own post."}, status=400)

        obj, created = VolunteerResponse.objects.get_or_create(
            post=post, volunteer=request.user, defaults={"status": "on_the_way"}
        )
        if created:
            # update counter quickly
            HelpPost.objects.filter(pk=post.pk).update(responders_count=post.responses.count())
            # notify author
            Notification.objects.create(
                user=post.author,
                actor=request.user,
                post=post,
                message=f"{request.user.username} is on the way to help your request: {post.title}",
            )
        serializer = VolunteerResponseSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """
        Author ends task -> marks post completed and credits all responders.
        Notifies volunteers and increments leaderboard.
        """
        post = self.get_object()
        if post.author_id != request.user.id:
            return Response({"detail": "Only the author can complete this task."}, status=403)
        if post.is_completed:
            return Response({"detail": "Already completed."}, status=200)

        with transaction.atomic():
            post.is_completed = True
            post.save(update_fields=["is_completed"])

            responders = list(post.responses.select_related("volunteer"))
            # credit each volunteer
            for resp in responders:
                if resp.status != "completed":
                    resp.status = "completed"
                    resp.save(update_fields=["status"])

                stat, _ = VolunteerStat.objects.get_or_create(user=resp.volunteer)
                stat.completed_count = stat.completed_count + 1
                stat.save(update_fields=["completed_count"])

                # notify volunteer
                Notification.objects.create(
                    user=resp.volunteer,
                    actor=request.user,
                    post=post,
                    message=f"Task '{post.title}' was marked completed. Your help has been counted!"
                )

        return Response({"detail": "Task completed and volunteers credited."}, status=200)

    @action(detail=False, methods=["get"])
    def leaderboard(self, request):
        """
        Top volunteers by completed_count
        """
        qs = VolunteerStat.objects.select_related("user").order_by("-completed_count", "user__username")[:50]
        data = LeaderboardEntrySerializer(qs, many=True).data
        return Response(data)
    

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_stats(self, request):
        """
        Return the current user's volunteer stats
        """
        stat, _ = VolunteerStat.objects.get_or_create(user=request.user)
        data = {
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            },
            "completed_count": stat.completed_count,
        }
        return Response(data)

class NotificationViewSet(mixins.ListModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """
    - GET /api/helpneed/notifications/  -> current user's notifications
    - PATCH /api/helpneed/notifications/<id>/ { "is_read": true }
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).select_related("user", "actor", "post").order_by("-created_at")
