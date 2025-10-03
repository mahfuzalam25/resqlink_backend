# safetyguide/serializers.py
from rest_framework import serializers
from .models import SafetyGuide, SafetyAdvice


class SafetyAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyAdvice
        fields = ['id', 'text']


class SafetyGuideSerializer(serializers.ModelSerializer):
    advices = SafetyAdviceSerializer(many=True, read_only=True)

    class Meta:
        model = SafetyGuide
        fields = ['id', 'icon', 'title', 'advices']
