from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import CommunitySection, Post, Comment
from .form import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.


def community_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(Q(section__section__icontains=q))

    sections = CommunitySection.objects.all()

    context = {
                'sections': sections,
                'posts': posts,
                }
    return render(request, 'community.html', context)


@login_required
def create_post(request):
    form = PostForm(user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('community')

    context = {'form': form}
    return render(request, 'post_form.html', context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('community')
    return render(request, 'delete.html', {'obj': post})


def view_post(request, pk,):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all()

    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        disliked = True

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        return redirect('post', pk=post.id)

    context = {
                'post': post,
                'post_comments': post_comments,
                'total_likes': total_likes,
                'total_dislikes': total_dislikes,
                'liked': liked,
                'disliked': disliked,
                }
    return render(request, 'post.html', context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('post', kwargs={'pk': post_pk}))
    return render(request, 'delete.html', {'obj': comment})


def like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    if post.likes.filter(pk=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        if post.dislikes.filter(pk=request.user.id).exists():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post', args=[str(pk)]))


def dislike_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    disliked = False
    if post.dislikes.filter(pk=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        if post.likes.filter(pk=request.user.id).exists():
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
        disliked = True

    return HttpResponseRedirect(reverse('post', args=[str(pk)]))


def error_404(request, exception):
    return render(request, '404.html', {})
