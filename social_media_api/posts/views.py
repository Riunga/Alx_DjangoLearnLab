from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed for the author of the post/comment
        return obj.author == request.user


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Set the user who created the post as the author
        serializer.save(author=self.request.user)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Set the user who created the comment as the author
        serializer.save(author=self.request.user)

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    to manage posts in the API.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        # Set the user who created the post as the author
        serializer.save(author=self.request.user)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author__in=self.request.user.following.all()).order_by('-created_at')

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like
from .serializers import LikeSerializer
from notifications.models import Notification

class LikePostView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Use the correct import for get_object_or_404
        post = get_object_or_404(Post, pk=kwargs['pk'])
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Use the correct import for get_object_or_404
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        like = get_object_or_404(Like, user=self.request.user, post=post)
        return like

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
class MarkNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        notifications.update(read=True)
        return Response({'message': 'Notifications marked as read'})
