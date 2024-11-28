from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics, viewsets, permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from blog.models import Post, Comment
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import PostSerializer, CommentSerializer, PostSerializerV2
from blog.throttling import PremiumUserRateThrottle


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    throttle_classes = (AnonRateThrottle, UserRateThrottle, PremiumUserRateThrottle)


class PostViewSetV2(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV2
    permission_classes = (IsAuthorOrReadOnly,)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(post=post)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        comment = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'post_{comment.post_id}',
            {
                'type': 'send_notification',
                'message': f'New comment {comment.author}: {comment.content}',
            }
        )
