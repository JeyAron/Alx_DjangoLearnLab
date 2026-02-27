from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed
from django.urls import path

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("feed/", feed, name="feed"),
]

urlpatterns += router.urls
