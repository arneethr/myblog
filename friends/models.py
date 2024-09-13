from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Friendship(models.Model):
    """
    Friendship model to handle friendships between users.
    """
    from_user = models.ForeignKey(User, related_name='friendships_sent_from_users', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendships_received_to_users', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friendship between {self.from_user} and {self.to_user}"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.created_at}"
