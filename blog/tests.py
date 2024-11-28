from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Post


class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_data = {
            'title': 'Post Title',
            'content': 'Post Content',
            'author': 'test_author',
        }

    def test_create_post(self):
        response = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        post = Post.objects.get(**self.post_data)
        self.client.force_authenticate(user=None)
        update_data = {"title": "Updated Title", "content": "Updated Content"}
        response = self.client.put(f'/api/posts/{post.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)