from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        return Response({"detail": "Post liked"}, status=status.HTTP_201_CREATED)
    return Response({"detail": "You already liked this post"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
    if deleted:
        return Response({"detail": "Post unliked"}, status=status.HTTP_200_OK)
    return Response({"detail": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, post=post)

        # Create notification
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id,
            )

        return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post)

        if not like.exists():
            return Response({"detail": "You haven't liked this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
