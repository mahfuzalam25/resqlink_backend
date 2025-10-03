from django.urls import path
from .views import EmergencyCallListView,StationInfoSearchView
urlpatterns = [
    path('calllist/', EmergencyCallListView.as_view(), name='emergency-call-list'),
    path('calllist/search/', StationInfoSearchView.as_view(), name='station-search'),
]
