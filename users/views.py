# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, FriendRequest, Follow
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, ProfileUpdateForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request, user_id):
    """
    View to display the profile of the user and options to add friends, follow, etc.
    """
    profile_user = get_object_or_404(User, id=user_id)
    sent_friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=profile_user).first()
    received_friend_request = FriendRequest.objects.filter(from_user=profile_user, to_user=request.user).first()
    is_following = Follow.objects.filter(follower=request.user, followed=profile_user).exists()

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user_id)
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'form': form,
        'sent_friend_request': sent_friend_request,
        'received_friend_request': received_friend_request,
        'is_following': is_following
    })

@login_required
def send_friend_request(request, user_id):
    """
    View to send a friend request to another user.
    """
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('profile', user_id=user_id)

@login_required
def accept_friend_request(request, user_id):
    """
    View to accept a friend request from another user.
    """
    from_user = get_object_or_404(User, id=user_id)
    friend_request = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    if friend_request:
        friend_request.is_accepted = True
        friend_request.save()
    return redirect('profile', user_id=user_id)

@login_required
def follow_user(request, user_id):
    """
    View to follow another user.
    """
    followed_user = get_object_or_404(User, id=user_id)
    Follow.objects.get_or_create(follower=request.user, followed=followed_user)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    """
    View to unfollow another user.
    """
    followed_user = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=request.user, followed=followed_user).first()
    if follow:
        follow.delete()
    return redirect('profile', user_id=user_id)
