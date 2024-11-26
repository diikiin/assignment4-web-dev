from django.db import models


class PostManager(models.Manager):
    def by_author(self, author):
        return self.get_queryset().filter(author=author)

    def by_category(self, category):
        return self.get_queryset().filter(categories=category)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='posts')
    image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True, null=True)

    objects = PostManager()

    def __str__(self):
        return f'Author: {self.author}, Title: {self.title}'


class Comment(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Author: {self.author}, Post: {self.post}'
