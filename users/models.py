from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model that adds a profile photo field.
    """
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_profile_photo_url(self):
        """
        Returns the profile photo URL or a default image if not provided.
        """
        if self.profile_photo:
            return self.profile_photo.url
        return '/static/images/default_profile.png'

    def friends(self):
        """
        Returns all users who are friends with this user.
        """
        friends_from = FriendRequest.objects.filter(from_user=self, is_accepted=True).values_list('to_user', flat=True)
        friends_to = FriendRequest.objects.filter(to_user=self, is_accepted=True).values_list('from_user', flat=True)
        return User.objects.filter(id__in=friends_from) | User.objects.filter(id__in=friends_to)

    def followers(self):
        """
        Returns all users who follow this user.
        """
        return Follow.objects.filter(followed=self).values_list('follower', flat=True)

    def following(self):
        """
        Returns all users this user is following.
        """
        return Follow.objects.filter(follower=self).values_list('followed', flat=True)


class FriendRequest(models.Model):
    """
    FriendRequest model to handle sending and accepting friend requests.
    """
    from_user = models.ForeignKey(User, related_name='friend_requests_sent_from_users', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received_to_users', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend request from {self.from_user} to {self.to_user}"


class Follow(models.Model):
    """
    Follow model to handle user following functionality.
    """
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
