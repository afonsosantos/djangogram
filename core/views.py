from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, ProfileForm, LoginForm, RegisterForm
from .models import Post, Like


@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.liked_by_user = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, 'core/feed.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    return render(request, 'core/create_post.html', {'form': form})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all().order_by('-created_at')

    return render(request, 'core/profile.html', {
        'profile_user': user,
        'posts': posts
    })


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return redirect('profile', username=user.username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileForm(instance=user.profile)

    return render(request, 'core/edit_profile.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': created
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('feed')
    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('feed')
    return render(request, 'core/register.html', {'form': form})
