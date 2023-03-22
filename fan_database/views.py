from django.shortcuts import render
from .models import Season
from .models import Episode


def index_view(request):
    seasons = Season.objects.all()
    context = {'seasons': seasons}
    return render(request, 'index.html', context)


def season_view(request):
    seasons = Season.objects.all()
    episodes = Episode.objects.all()
    context = {
                'seasons': seasons,
                'episodes': episodes
                }
    return render(request, 'season.html', context)


