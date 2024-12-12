from django.db import models
from django.contrib.auth.models import User


class Repo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    notes_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Commit(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    note_title = models.CharField(max_length=100, null=True, blank=True)
    note_body = models.TextField(null=True, blank=True)
