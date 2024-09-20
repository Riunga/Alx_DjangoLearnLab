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

# posts/views.py
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404  # Import this to use get_object_or_404
from .models import Post
from .serializers import PostSerializer

# Post ViewSet to handle CRUD operations for posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # Retrieve a post by primary key using get_object_or_404
    def retrieve(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)  # Ensure this line is present
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Method to like a post
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)  # Using get_object_or_404 to retrieve the post
        # Logic to handle liking the post (e.g., add the user to the likes)
        post.likes.add(request.user)
        return Response({'message': 'Post liked successfully'}, status=status.HTTP_200_OK)

    # Method to unlike a post
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)  # Using get_object_or_404 to retrieve the post
        # Logic to handle unliking the post (e.g., remove the user from the likes)
        post.likes.remove(request.user)
        return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)

class MarkNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        notifications.update(read=True)
        return Response({'message': 'Notifications marked as read'})
