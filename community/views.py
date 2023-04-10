from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import CommunitySection, Post, Comment
from .form import PostForm

# Create your views here.


def community_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(Q(section__section__icontains=q))

    sections = CommunitySection.objects.all()

    context = {'sections': sections, 'posts': posts}
    return render(request, 'community.html', context)


def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('community')

    context = {'form': form}
    return render(request, 'post_form.html', context)


def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('community')
    return render(request, 'delete.html', {'obj': post})


def view_post(request, pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all()
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        return redirect('post', pk=post.id)

    context = {'post': post, 'post_comments': post_comments}
    return render(request, 'post.html', context)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('post', kwargs={'pk': post_pk}))
    return render(request, 'delete.html', {'obj': comment})


def error_404(request, exception):
    return render(request, '404.html', {})
    