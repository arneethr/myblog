# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, BlogPostViewSet, CommentViewSet, LikeViewSet, FriendRequestViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', BlogPostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'friend-requests', FriendRequestViewSet)
router.register(r'follows', FollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
