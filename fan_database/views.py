from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from .models import Season, Episode, EpisodeLog, ApprovalRequest
from .form import EpisodeForm, RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup


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
            plot_html = request.POST.get('plot', '')
            plot_text = BeautifulSoup(
                                            plot_html,
                                            'html.parser').get_text().strip()

            if len(plot_text) == 0:
                form.add_error(
                                'plot',
                                ValidationError("Plot cannot be empty"))
            else:
                episode = form.save(commit=False)
                form.save()
                # create an approval request for the created episode
                reason = form.cleaned_data.get('reason')
                approval_request = ApprovalRequest(
                    user=request.user,
                    object_to_approve=episode,
                    request_type='approval',
                    reason=reason
                )
                approval_request.save()

                season_value = request.POST.get('season')
                url = reverse('Season', args=[season_value])
                messages.success(
                        request,
                        'Your request to add an episode has been submitted.'
                        )
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
            plot_html = request.POST.get('plot', '')
            plot_text = BeautifulSoup(
                                            plot_html,
                                            'html.parser').get_text().strip()

            if len(plot_text) == 0:
                form.add_error(
                                'plot',
                                ValidationError("Plot cannot be empty"))
            else:
                # create a log entry for the unedited episode
                og_episode = Episode.objects.get(id=pk)
                EpisodeLog.objects.create(
                    episode=original_episode,
                    overall_episode_number=og_episode.overall_episode_number,
                    season_episode_number=og_episode.season_episode_number,
                    season=og_episode.season,
                    title=og_episode.title,
                    synopsis=og_episode.synopsis,
                    plot=og_episode.plot,
                    air_date=og_episode.air_date,
                    stardate=og_episode.stardate,
                    approved=True
                )
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
                messages.success(
                                request,
                                'Update request submitted successfully.'
                                )
                return redirect(reverse('Season', kwargs={'pk': season_id}))
    context = {'form': form}
    return render(request, 'episode_form.html', context)


@login_required(login_url='login')
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def approve_add_request_confirm(request, pk):
    approval_request = get_object_or_404(ApprovalRequest, pk=pk)
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
            messages.error(request, 'Add request successfully.')
            return redirect('admin-request')

    context = {
            'approval_request': approval_request,
            'reason': approval_request.reason,
            'episode_data': episode
            }
    return render(request, 'approve_add_request_confirm.html', context)


@user_passes_test(lambda u: u.is_superuser)
def reject_add_request_confirm(request, pk):
    approval_request = get_object_or_404(ApprovalRequest, pk=pk)
    episode = approval_request.object_to_approve
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            approval_request.delete()
            messages.error(request, 'Add request rejected')
            return redirect('admin-request')
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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
            # Reload the episode object from the
            # EpisodeLog model to get the original state
            original_episode = EpisodeLog.objects.filter(
                episode=episode,
                approved=True
            ).order_by('-timestamp').first()
            # Create a new instance of EpisodeLog with the original data
            episode_log = EpisodeLog.objects.create(
                episode=episode,
                overall_episode_number=original_episode.overall_episode_number,
                season_episode_number=original_episode.season_episode_number,
                season=original_episode.season,
                title=original_episode.title,
                synopsis=original_episode.synopsis,
                plot=original_episode.plot,
                air_date=original_episode.air_date,
                stardate=original_episode
                .stardate,
                approved=True
            )
            # Update the original episode object
            # with the data from the episode_log instance
            episode.overall_episode_number = episode_log.overall_episode_number
            episode.season_episode_number = episode_log.season_episode_number
            episode.season = episode_log.season
            episode.title = episode_log.title
            episode.synopsis = episode_log.synopsis
            episode.plot = episode_log.plot
            episode.air_date = episode_log.air_date
            episode.stardate = episode_log.stardate
            episode.approved = True
            episode.save()
            edit_request.delete()
            messages.success(request, 'Update request rejected.')
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


@user_passes_test(lambda u: u.is_superuser)
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
    context = {
            'delete_request': delete_request,
            'episode': episode,
            'reason': delete_request.reason
        }
    return render(request, 'approve_delete_request_confirm.html', context)


@user_passes_test(lambda u: u.is_superuser)
def reject_delete_request_confirm(request, pk):
    delete_request = get_object_or_404(ApprovalRequest, pk=pk)
    episode = delete_request.object_to_approve
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('reject_confirm'):
            delete_request.delete()
            messages.success(request, 'The delete request has been rejected.')
            return redirect('admin-request')
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
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('Home')
    else:
        form = RegisterForm()
        messages.error(request, 'An error occured during registration')

    return render(request, 'registration/sign_up.html', {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Username or Password does not exist')

    return render(request, 'registration/login.html', {"form": form})


@user_passes_test(lambda u: u.is_superuser)
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')


@user_passes_test(lambda u: u.is_superuser)
def password_change_form(request):
    return render(request, 'registration/password_change_form.html')


@user_passes_test(lambda u: u.is_superuser)
def password_reset_form(request):
    return render(request, 'registration/password_reset_form.html')


@user_passes_test(lambda u: u.is_superuser)
def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


@user_passes_test(lambda u: u.is_superuser)
def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html')


@user_passes_test(lambda u: u.is_superuser)
def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')


def error_404(request, exception):
    return render(request, '404.html', {})
