from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    avatar_url = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email