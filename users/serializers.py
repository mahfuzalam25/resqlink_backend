from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Location, Experience, Education, Certification

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['home_address', 'office_address', 'city', 'district', 'division', 'zip_code']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['experience_title', 'duration', 'organization_name', 'organization_address', 'description']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['institution_name', 'duration', 'department_name', 'institution_address']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['certificate_title', 'year', 'description']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    location = LocationSerializer()
    experience = ExperienceSerializer()
    education = EducationSerializer()
    certification = CertificationSerializer()

    class Meta:
        model = Profile
        fields = [
            'url', 'id', 'user', 'bio', 'blood_group', 'image', 'phone',
            'location', 'experience', 'education', 'certification',
        ]

    def update(self, instance, validated_data):
        nested_serializers = {
            'location': LocationSerializer,
            'experience': ExperienceSerializer,
            'education': EducationSerializer,
            'certification': CertificationSerializer,
        }

        # Handle nested model updates
        for field, serializer_class in nested_serializers.items():
            nested_data = validated_data.pop(field, None)
            if nested_data:
                nested_instance = getattr(instance, field)
                serializer = serializer_class(nested_instance, data=nested_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        # Update remaining profile fields
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)  # Now writable
    old_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name',
                  'password', 'old_password', 'profile']

    def validate_email(self, value):
        if self.instance is None:  # Signup
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email is already in use.")
        else:  # Update
            if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if profile_data:
            Profile.objects.update_or_create(user=user, defaults=profile_data)

        return user

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Handle password change
        if 'password' in validated_data:
            password = validated_data.pop('password')
            old_password = validated_data.pop('old_password', None)
            if old_password and instance.check_password(old_password):
                instance.set_password(password)
            elif old_password is None:
                raise serializers.ValidationError({"info": "Old password is required."})
            else:
                raise serializers.ValidationError({"info": "Old password is incorrect."})

        # Handle nested profile update
        profile_data = validated_data.pop('profile', None)
        if profile_data and hasattr(instance, 'profile'):
            profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, data):
        method = self.context['request'].method
        password = data.get('password', None)

        if method == 'POST':
            if not password:
                raise serializers.ValidationError({"info": "Please provide a password."})
        elif method in ['PUT', 'PATCH']:
            if password and not data.get('old_password'):
                raise serializers.ValidationError({"info": "Please provide the old password to set a new one."})
        return data
