from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Organization
from .serializers import OrganizationSerializer

class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrganizationSerializer(
            data=request.data,
            context={"request": request}  # IMPORTANT
        )

        if serializer.is_valid():
            org = serializer.save()
            return Response(
                OrganizationSerializer(org).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)


class OrganizationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # all orgs where user is a member
        orgs = Organization.objects.filter(
            memberships__user=request.user
        ).distinct()

        serializer = OrganizationSerializer(orgs, many=True)
        return Response(serializer.data)