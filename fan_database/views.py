from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Season, Episode
from .form import EpisodeForm, RegisterForm
from django.contrib.auth import login


def index_view(request):
    return render(request, 'index.html')


def display_season_all_pages(request):
    seasons = Season.objects.all()
    return {'seasons': seasons}


def season_view(request, season_id):
    episodes = Episode.objects.filter(season=season_id)
    context = {'episodes': episodes}
    return render(request, 'season.html', context)


def episode_view(request, episode_id):
    episode = Episode.objects.get(pk=episode_id)
    context = {'episode': episode}
    return render(request, 'episode.html', context)


@login_required(login_url='login')
def add_episode(request):
    form = EpisodeForm()

    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Season')

    context = {'form': form}
    return render(request, 'episode_form.html', context)


@login_required(login_url='login')
def update_episode(request, pk):
    episode = Episode.objects.get(id=pk)
    form = EpisodeForm(instance=episode)

    if request.method == 'POST':
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            form.save()
            return redirect('Season')

    context = {'form': form}
    return render(request, 'episode_form.html', context)


@login_required(login_url='login')
def delete_episode(request, pk):
    episode = get_object_or_404(Episode, id=pk)
    if request.method == 'POST':
        episode.delete()
        return redirect('Season')
    return render(request, 'delete.html', {'obj': episode})


def search_query(request):
    if request.method == "POST":
        searched = request.POST['searched']
        episodes = Episode.objects.filter(title__icontains=searched)
        context = {'searched': searched, 'episodes': episodes}
        return render(request, 'search_query.html', context)
    else:
        return render(request, 'search_query.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
