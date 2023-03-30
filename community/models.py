from django.db import models
from django.contrib.auth.models import User


class CommunitySection(models.Model):
    section = models.CharField(max_length=200)

    def __str__(self):
        return self.section


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(CommunitySection, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

