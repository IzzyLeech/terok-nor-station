from django.shortcuts import render, redirect
from .models import Season
from .models import Episode
from .form import EpisodeForm


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


def add_episode(request):
    form = EpisodeForm()

    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Season')

    context = {'form': form}
    return render(request, 'episode_form.html', context)
