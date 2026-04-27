from django.db import models
from django.conf import settings

# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    org = models.ForeignKey(
        'organizations.Organization', on_delete=models.CASCADE, related_name='projects'
    )
    slug = models.SlugField(max_length=63)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('org', 'slug')]

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships'
    )
    role = models.CharField(max_length=20, default='member')
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_project_members'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('project', 'user')]

    def __str__(self):
        return f"{self.user} - {self.project} ({self.role})"
