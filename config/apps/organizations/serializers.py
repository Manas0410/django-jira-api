from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, OrgMembership

User = get_user_model()

class OrgMembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # shows username/email via __str__

    class Meta:
        model = OrgMembership
        fields = ["id", "user", "role", "joined_at"]

class OrganizationSerializer(serializers.ModelSerializer):
    # nested memberships for GET
    memberships = OrgMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "slug",
            "name",
            "logo_url",
            "created_by",
            "is_active",
            "created_at",
            "updated_at",
            "memberships",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Called when serializer.save() is used in POST
        """
        request = self.context.get("request")
        user = request.user  # logged-in user

        # 1. create org
        org = Organization.objects.create(
            created_by=user,
            **validated_data
        )

        # 2. auto-add creator as admin
        OrgMembership.objects.create(
            org=org,
            user=user,
            role="admin",
            invited_by=user,
            joined_at=org.created_at
        )

        return org