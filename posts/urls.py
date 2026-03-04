from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = []
urlpatterns += [
    path("feed/", feed, name="feed"),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
]

urlpatterns += router.urls
