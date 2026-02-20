from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
