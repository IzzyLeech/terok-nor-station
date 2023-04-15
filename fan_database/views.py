from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from .models import Season, Episode, ApprovalRequest
from .form import EpisodeForm, RegisterForm
from django.contrib.auth import login


def index_view(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)


def display_season_all_pages(request):
    seasons = Season.objects.all()
    return {'seasons': seasons}


def season_view(request, pk):
    current_season = get_object_or_404(Season, pk=pk)
    episodes = Episode.objects.filter(season=current_season, approved=True)

    context = {
        'current_season': current_season,
        'episodes': episodes,
    }
    return render(request, 'season.html', context)


def episode_view(request, episode_id):
    episode = Episode.objects.get(pk=episode_id)
    context = {'episode': episode}
    return render(request, 'episode.html', context)


@login_required(login_url='login')
def add_episode(request):
    form = EpisodeForm()
    episode = None

    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            episode = form.save(commit=False)
            form.save()
            # create an approval request for the created episode
            reason = form.cleaned_data.get('reason')
            approval_request = ApprovalRequest(
                user=request.user,
                object_to_approve=episode,
                request_type='approval',
                reason=reason,
            )
            approval_request.save()

            season_value = request.POST.get('season')
            url = reverse('Season', args=[season_value])
            return redirect(url)

    context = {'form': form, 'episode_data': episode}
    return render(request, 'episode_form.html', context)


@login_required(login_url='login')
def update_episode(request, pk):
    episode = get_object_or_404(Episode, id=pk)
    form = EpisodeForm(instance=episode)
    season_id = episode.season.pk

    if request.method == 'POST':
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.approved = False
            episode.save()
            # create an approval request for the edited episode
            reason = form.cleaned_data.get('reason')
            ApprovalRequest.objects.create(
                object_to_approve=episode,
                user=request.user,
                request_type='edit',
                reason=reason,
            )
            messages.success(request, 'Update request submitted successfully.')
            return redirect(reverse('Season', kwargs={'pk': season_id}))
    context = {'form': form}
    return render(request, 'episode_form.html', context)


def delete_episode(request, pk):
    episode = get_object_or_404(Episode, id=pk)
    season_id = episode.season.pk
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if not reason:
            messages.error(
                            request,
                            'Please provide a reason for the deletion.'
                            )
            return redirect(reverse('delete-episode', kwargs={'pk': pk}))
        approval_request = ApprovalRequest(
            user=request.user,
            object_to_approve=episode,
            request_type='delete',
            reason=reason
        )
        approval_request.save()
        return redirect(reverse('Season', kwargs={'pk': season_id}))
    return render(request, 'delete_request.html', {'obj': episode})


def admin_request(request):
    delete_requests = ApprovalRequest.objects.filter(
                                                    approved=False,
                                                    request_type='delete'
                                                    )
    approval_requests = ApprovalRequest.objects.filter(
                                                        approved=False,
                                                        request_type='approval'
                                                        )
    edit_requests = ApprovalRequest.objects.filter(
                                                    approved=False,
                                                    request_type='edit'
                                                    )
    context = {
                'delete_requests': delete_requests,
                'approval_requests': approval_requests,
                'edit_requests': edit_requests,
                }
    return render(request, 'admin_request.html', context)


def add_request(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # redirect to approval confirm page
            # with approval request pk as parameter
            return redirect('approve_add_request_confirm')
        elif action == 'reject':
            # redirect to reject confirm page with
            # approval request pk as parameter
            return redirect('reject_add_request_confirm')
        return redirect('admin-request')


def approve_add_request_confirm(request, pk):
    approval_request = get_object_or_404(
                                        ApprovalRequest,
                                        pk=pk,
                                        )
    episode = approval_request.object_to_approve
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('approve_confirm'):
            approval_request.approved = True
            # Mark the created episode as approved
            approval_request.object_to_approve.approved = True
            # Save the created episode to the database
            approval_request.object_to_approve.save()
            approval_request.save()
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    context = {
                'approval_request': approval_request,
                'reason': approval_request.reason,
                'episode_data': episode
                }
    return render(request, 'approve_add_request_confirm.html', context)


def reject_add_request_confirm(request, pk):
    approval_request = get_object_or_404(
                                        ApprovalRequest,
                                        pk=pk,
                                        )
    episode = approval_request.object_to_approve
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            approval_request.delete()
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    context = {
        'approval_request': approval_request,
        'reason': approval_request.reason,
        'episode_data': episode,
        }
    return render(request, 'reject_add_request_confirm.html', context)


def edit_request(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # redirect to approval confirm page
            # with approval request pk as parameter
            return redirect('approve_edit_request_confirm')
        elif action == 'reject':
            # redirect to reject confirm page
            # with approval request pk as parameter
            return redirect('reject_edit_request_confirm')
        return redirect('admin-request')


def approve_edit_request_confirm(request, pk):
    edit_request = get_object_or_404(
                                    ApprovalRequest,
                                    id=pk,
                                    request_type='edit'
                                    )
    episode = edit_request.object_to_approve

    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('approve_confirm'):
            episode.approved = True
            episode.save()
            edit_request.delete()
            messages.success(request, 'Update approved successfully.')

            return redirect('admin-request')

    context = {
        'edit_request': edit_request,
        'episode': episode,
        'reason': edit_request.reason,
    }
    return render(request, 'approve_edit_request_confirm.html', context)


def reject_edit_request_confirm(request, pk):
    edit_request = get_object_or_404(
                                    ApprovalRequest,
                                    id=pk,
                                    request_type='edit'
                                    )
    episode = edit_request.object_to_approve

    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            # Reload the episode object from
            # the database to get the original state
            episode = Episode.objects.get(id=episode.id)
            episode.approved = True
            # Mark the original object not approved
            episode.save()
            edit_request.delete()
            messages.success(request, 'Update rejected.')
            return redirect('admin-request')

    context = {
        'edit_request': edit_request,
        'episode': episode,
        'reason': edit_request.reason,
    }
    return render(request, 'reject_edit_request_confirm.html', context)


def delete_request(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # redirect to approval confirm page with
            #  delete request pk as parameter
            return redirect('approve_delete_request_confirm',)
        elif action == 'reject':
            # redirect to reject confirm page with
            # delete request pk as parameter
            return redirect('reject_delete_request_confirm')
        else:
            messages.error(request, 'Invalid action.')
    return render(request, 'admin_request.html')


def approve_delete_request_confirm(request, pk):
    delete_request = get_object_or_404(
                                        ApprovalRequest,
                                        pk=pk,
                                        request_type='delete'
                                        )
    episode = delete_request.object_to_approve
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('approve_confirm'):
            # approve the delete request
            delete_request.approved = True
            delete_request.save()
            delete_request.object_to_approve.delete()
            messages.success(request, 'The delete request has been approved.')
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    context = {
                'delete_request': delete_request,
                'episode': episode,
                'reason': delete_request.reason
                }
    return render(request, 'approve_delete_request_confirm.html', context)


def reject_delete_request_confirm(request, pk):
    delete_request = get_object_or_404(ApprovalRequest, pk=pk)
    episode = delete_request.object_to_approve
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            delete_request.delete()
            messages.success(request, 'The delete request has been rejected.')
            return redirect('admin-request')
        else:
            messages.error(request, 'Invalid action.')
    context = {
                'delete_request': delete_request,
                'episode': episode,
                'reason': delete_request.reason
                }
    return render(request, 'reject_delete_request_confirm.html', context)


def search_query(request):
    if request.method == "POST":
        searched = request.POST['searched']
        episodes = Episode.objects.filter(title__icontains=searched)
        if not episodes:
            message = 'No items found for "{}".'.format(searched)
        else:
            message = 'Search results for "{}":'.format(searched)
        context = {
                    'searched': searched,
                    'episodes': episodes,
                    'message': message
                    }
        return render(request, 'search_query.html', context)
    else:
        context = {'searched': None, 'episodes': None, 'message': None}
        return render(request, 'search_query.html', context)


def sign_up(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
    else:
        form = RegisterForm()
        messages.error(request, 'An error occured during registration')

    return render(request, 'registration/sign_up.html', {"form": form})


def error_404(request, exception):
    return render(request, '404.html', {})
