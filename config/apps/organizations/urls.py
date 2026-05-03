from django.urls import path
from .views import OrganizationCreateView, OrganizationListView, OrganizationDetailView

urlpatterns = [
    path("create-org/", OrganizationCreateView.as_view()),  # POST
    path("get-orgs/", OrganizationListView.as_view()),    # GET
    path("<int:pk>/", OrganizationDetailView.as_view()),
]