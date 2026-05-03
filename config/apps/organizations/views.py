from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Organization
from .serializers import OrganizationSerializer
from .permissions import IsOrgAdmin

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



class OrganizationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return None

    #  get by id 
    def get(self, request, pk):
        org = self.get_object(pk)

        if not org:
            return Response({"error": "Not found"}, status=404)

        serializer = OrganizationSerializer(org)
        return Response(serializer.data)

    # update by id
    def patch(self, request, pk):
        org = self.get_object(pk)

        if not org:
            return Response({"error": "Not found"}, status=404)

        # 🔐 check admin permission
        if not IsOrgAdmin().has_object_permission(request, self, org):
            return Response({"error": "Not allowed"}, status=403)

        serializer = OrganizationSerializer(
            org,
            data=request.data,
            partial=True  # important for PATCH
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
        
    # delete by id 
    
    def delete(self, request, pk):
        org = self.get_object(pk)

        if not org:
            return Response({"error": "Not found"}, status=404)

        # 🔐 admin only
        if not IsOrgAdmin().has_object_permission(request, self, org):
            return Response({"error": "Not allowed"}, status=403)

        org.delete()
        return Response({"message": "Deleted successfully"}, status=204)