# safetyguide/views.py
from rest_framework import generics
from .models import SafetyGuide
from .serializers import SafetyGuideSerializer


class SafetyGuideListView(generics.ListAPIView):
    queryset = SafetyGuide.objects.all()
    serializer_class = SafetyGuideSerializer
