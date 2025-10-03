from rest_framework import routers
from .viewsets import UserViewset, ProfileViewSet

app_name = "users"
router = routers.DefaultRouter()
router.register('users',UserViewset)
router.register('profiles', ProfileViewSet)