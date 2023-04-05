from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import Season, Episode, DeleteRequest
from .form import EpisodeForm, RegisterForm
from django.contrib.auth import login


def index_view(request):
    return render(request, 'index.html')


def display_season_all_pages(request):
    seasons = Season.objects.all()
    return {'seasons': seasons}


def season_view(request, pk):
    season = get_object_or_404(Season, pk=pk)
    episodes = season.episode_set.all()
    context = {'episodes': episodes, 'season': season}
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
            season_value = request.POST.get('season')
            url = reverse('Season', args=[season_value])
            return redirect(url)

    context = {'form': form}
    return render(request, 'episode_form.html', context)


@login_required(login_url='login')
def update_episode(request, pk):
    episode = get_object_or_404(Episode, id=pk)
    form = EpisodeForm(instance=episode)
    season_id = episode.season.pk

    if request.method == 'POST':
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            form.save()
            return redirect(reverse('Season', kwargs={'pk': season_id}))

    context = {'form': form}
    return render(request, 'episode_form.html', context)


def delete_episode(request, pk):
    episode = get_object_or_404(Episode, id=pk)
    season_id = episode.season.pk
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if not reason:
            messages.error(request, 'Please provide a reason for the deletion.')
            return redirect(reverse('delete_episode', kwargs={'pk': pk}))
        delete_request = DeleteRequest(user=request.user, object_to_delete=episode, reason=reason)
        delete_request.save()
        return redirect(reverse('Season', kwargs={'pk': season_id}))
    return render(request, 'delete.html', {'obj': episode})


@user_passes_test(lambda u: u.is_superuser)
def delete_request_list(request):
    delete_requests = DeleteRequest.objects.filter(approved=False)
    return render(request, 'delete_request.html', {'delete_requests': delete_requests})


@user_passes_test(lambda u: u.is_superuser)
def approve_delete_request(request, pk):
    delete_request = get_object_or_404(DeleteRequest, pk=pk)
    delete_request_approved = True
    delete_request.save()
    delete_request.object_to_delete.delete()
    return redirect('Home')


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
