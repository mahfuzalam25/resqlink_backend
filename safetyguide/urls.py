# safetyguide/urls.py
from django.urls import path
from .views import SafetyGuideListView

urlpatterns = [
    path('guides/', SafetyGuideListView.as_view(), name='safety-guide-list'),
]
