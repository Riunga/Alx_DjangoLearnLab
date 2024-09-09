from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]

from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),  # List all posts
    path('posts/new/', PostCreateView.as_view(), name='post-create'),  # Create new post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View a single post
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),  # Edit a post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete a post
]
