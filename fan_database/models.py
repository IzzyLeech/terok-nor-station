from django.db import models


class Season(models.Model):
    season_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    episode_count = models.IntegerField()

    def __str__(self):
        return self.season_number


class Episode(models.Model):
    overall_episode_number = models.IntegerField()
    season_episode_number = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    air_date = models.DateField()
    stardate = models.IntegerField()
