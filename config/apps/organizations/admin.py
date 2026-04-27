from django.contrib import admin
from .models import Organization, OrgMembership, ActivityLog

admin.site.register(Organization)
admin.site.register(OrgMembership)
admin.site.register(ActivityLog)