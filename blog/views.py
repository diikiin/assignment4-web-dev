from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog.models import Post, Comment
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import PostSerializer, CommentSerializer, PostSerializerV2
from blog.throttling import PremiumUserRateThrottle


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthorOrReadOnly,)
    throttle_classes = (AnonRateThrottle, UserRateThrottle, PremiumUserRateThrottle)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSetV2(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV2
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthorOrReadOnly,)
    throttle_classes = (AnonRateThrottle, UserRateThrottle, PremiumUserRateThrottle)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        comment = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'post_{comment.post.id}',
            {
                'type': 'send_notification',
                'message': f'New comment by {comment.author}: {comment.content}'
            }
        )
