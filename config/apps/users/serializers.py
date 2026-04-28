from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    avatar_url = serializers.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'avatar_url']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        avatar_url = validated_data.pop('avatar_url', None)

        # Create user
        user = User.objects.create_user(**validated_data)

        # Update profile (created via signal)
        profile = user.userprofile
        profile.full_name = full_name
        profile.avatar_url = avatar_url
        profile.save()

        return user