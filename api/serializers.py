from rest_framework import serializers
from blog.models import BlogPost, Comment, Like
from users.models import User, FriendRequest, Follow

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_photo']

class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogPost model.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'image', 'video', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    """
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'post', 'user']

class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model.
    """
    from_user = UserSerializer(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'is_accepted']

class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for Follow model.
    """
    follower = UserSerializer(read_only=True)
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed']
