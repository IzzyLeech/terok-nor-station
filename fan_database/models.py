from django.db import models
from django.contrib.auth.models import User


class Season(models.Model):
    season_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    episode_count = models.IntegerField()

    class Meta:
        ordering = ['season_number']

    def __str__(self):
        return str(self.season_number)


class Episode(models.Model):
    overall_episode_number = models.IntegerField()
    season_episode_number = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    synopsis = models.TextField(default="Enter synopsis for episode")
    air_date = models.DateField()
    stardate = models.DecimalField(max_digits=6, decimal_places=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['season_episode_number']

    def __str__(self):
        return self.title


class ApprovalRequest(models.Model):
    REQUEST_TYPES = (
        ('approval', 'Approval'),
        ('edit', 'Edit'),
        ('delete', 'Delete')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_to_approve = models.ForeignKey(Episode, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    reason = models.TextField(default="Enter inforamtion on the request")
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES,)
