from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from .models import Friendship, Follow, Message
from .forms import MessageForm

User = get_user_model()

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    # Avoid sending duplicate friend requests
    if not Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():
        Friendship.objects.create(from_user=request.user, to_user=to_user)
    return redirect('profile', user_id=user_id)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    if friend_request.is_accepted:
        return HttpResponseForbidden("This friend request has already been accepted.")
    friend_request.is_accepted = True
    friend_request.save()
    return redirect('profile', user_id=friend_request.from_user.id)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
    if follow:
        follow.delete()
    return redirect('profile', user_id=user_id)

@login_required
def send_message(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('profile', user_id=user_id)
    else:
        form = MessageForm()
    return render(request, 'friends/send_message.html', {'form': form, 'recipient': recipient})

@login_required
def message_list(request):
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'friends/message_list.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })
