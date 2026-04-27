from django.db import models
from django.conf import settings

# Create your models here.
class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=63, unique=True)
    name = models.CharField(max_length=150)
    logo_url = models.URLField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_organizations'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrgMembership(models.Model):
    id = models.AutoField(primary_key=True)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='memberships'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='org_memberships'
    )
    role = models.CharField(max_length=20, default='member')
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_invites'
    )
    joined_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('org', 'user')]

    def __str__(self):
        return f"{self.user} - {self.org} ({self.role})"


class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='activity_logs'
    )
    entity_type = models.CharField(max_length=50, db_index=True)
    entity_id = models.IntegerField(db_index=True)
    action = models.CharField(max_length=50)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.actor} {self.action} {self.entity_type}:{self.entity_id}"

