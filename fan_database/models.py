from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Season(models.Model):
    season_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    episode_count = models.IntegerField()
    image = CloudinaryField("image", default='placeholder')
    summary = models.TextField(default='Enter an summary on what happen in the season')

    class Meta:
        ordering = ['season_number']

    @property
    def next_season(self):
        return Season.objects.filter(season_number__gt=self.season_number).order_by('season_number').first()

    @property
    def previous_season(self):
        return Season.objects.filter(season_number__lt=self.season_number).order_by('-season_number').first()

    def __str__(self):
        return str(self.season_number)


class Episode(models.Model):
    overall_episode_number = models.IntegerField()
    season_episode_number = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    image = CloudinaryField("image", default="placeholder")
    synopsis = models.TextField(default="Enter synopsis for episode, keep it brief and in one paragraph")
    plot = models.TextField(default="Write a detail description of the episode's plot, use multiple paragraphs")
    air_date = models.DateField()
    stardate = models.DecimalField(max_digits=6, decimal_places=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['season_episode_number']

    def __str__(self):
        return self.title


class EpisodeLog(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    overall_episode_number = models.IntegerField()
    season_episode_number = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    synopsis = models.TextField()
    air_date = models.DateField()
    stardate = models.DecimalField(max_digits=6, decimal_places=1)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.episode} ({self.timestamp})'


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
