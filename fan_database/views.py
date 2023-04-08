from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from .models import Season, Episode, DeleteRequest, ApprovalRequest
from .form import EpisodeForm, RegisterForm
from django.contrib.auth import login


def index_view(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)


def display_season_all_pages(request):
    seasons = Season.objects.all()
    return {'seasons': seasons}


def season_view(request, pk):
    season = get_object_or_404(Season, pk=pk)
    episodes = season.episode_set.filter(approved=True)
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
            episode = form.save(commit=False)
            form.save()

            approval_request = ApprovalRequest(
                user=request.user,
                object_to_approve=episode,
            )
            approval_request.save()

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


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def admin_request(request):
    delete_requests = DeleteRequest.objects.filter(approved=False)
    approval_requests = ApprovalRequest.objects.filter(approved=False)
    context = {'delete_requests': delete_requests, 'approval_requests': approval_requests}
    return render(request, 'admin_request.html', context)


def add_request(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # redirect to approval confirm page with approval request pk as parameter
            return redirect('approve_add_request_confirm')
        elif action == 'reject':
            # redirect to reject confirm page with approval request pk as parameter
            return redirect('reject_add_request_confirm')
        return redirect('admin-request')


def approve_add_request_confirm(request, pk):
    approval_request = get_object_or_404(ApprovalRequest, pk=pk)
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('approve_confirm'):
            approval_request.approved = True
            approval_request.object_to_approve.approved = True  # Mark the created episode as approved
            approval_request.object_to_approve.save()  # Save the created episode to the database
            approval_request.save()
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    return render(request, 'approve_add_request_confirm.html', {'approval_request': approval_request})


def reject_add_request_confirm(request, pk):
    approval_request = get_object_or_404(ApprovalRequest, pk=pk)
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            approval_request.delete()
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    return render(request, 'reject_add_request_confirm.html', {'approval_request': approval_request})


def delete_request(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # redirect to approval confirm page with delete request pk as parameter
            return redirect('approve_delete_request_confirm',)
        elif action == 'reject':
            # redirect to reject confirm page with delete request pk as parameter
            return redirect('reject_delete_request_confirm')
        else:
            messages.error(request, 'Invalid action.')
    return render(request, 'admin_request.html')


def approve_delete_request_confirm(request, pk):
    delete_request = get_object_or_404(DeleteRequest, pk=pk)
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('approve_confirm'):
            # approve the delete request and delete the object
            delete_request.approved = True
            delete_request.save()
            delete_request.object_to_delete.delete()
            messages.success(request, 'The delete request has been approved.')
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    return render(request, 'approve_delete_request_confirm.html', {'delete_request': delete_request})


def reject_delete_request_confirm(request, pk):
    delete_request = get_object_or_404(DeleteRequest, pk=pk)
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            delete_request.delete()
            messages.success(request, 'The delete request has been rejected.')
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    return render(request, 'reject_delete_request_confirm.html', {'delete_request': delete_request})


def search_query(request):
    if request.method == "POST":
        searched = request.POST['searched']
        episodes = Episode.objects.filter(title__icontains=searched)
        if not episodes:
            message = 'No items found for "{}".'.format(searched)
        else:
            message = 'Search results for "{}":'.format(searched)
        context = {'searched': searched, 'episodes': episodes, 'message': message}
        return render(request, 'search_query.html', context)
    else:
        context = {'searched': None, 'episodes': None, 'message': None}
        return render(request, 'search_query.html', context)


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
