from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HelpPostViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'posts', HelpPostViewSet, basename='helppost')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
