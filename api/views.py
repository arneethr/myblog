# api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BlogPostSerializer, CommentSerializer, LikeSerializer, UserSerializer, FriendRequestSerializer, FollowSerializer
from blog.models import BlogPost, Comment, Like
from users.models import User, FriendRequest, Follow
from .permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing, creating, editing, and deleting blog posts.
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing, creating, and deleting comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating likes on blog posts.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing friend requests.
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing follows.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
