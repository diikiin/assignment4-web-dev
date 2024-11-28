from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet, CommentViewSet, PostViewSetV2

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('comments', CommentViewSet, basename='comments')

router_v2 = DefaultRouter()
router_v2.register('posts', PostViewSetV2, basename='posts-v2')

urlpatterns = [
    path('v1/', include((router_v1.urls, 'v1'), namespace='v1')),
    path('v2/', include((router_v2.urls, 'v2'), namespace='v2')),
]
