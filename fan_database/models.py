from django.db import models


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

    class Meta:
        ordering = ['season_episode_number']

    def __str__(self):
        return self.title
