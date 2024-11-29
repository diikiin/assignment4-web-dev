from django.urls import path

from blog.consumer import CommentConsumer

websocket_urlpatterns = [
    path('ws/comments/<int:post_id>/', CommentConsumer.as_asgi()),
]