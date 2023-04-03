from django.shortcuts import render, redirect
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
            form.save()
            return redirect('community')

    context = {'form': form}
    return render(request, 'post_form.html', context)


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
