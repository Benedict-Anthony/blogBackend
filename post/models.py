from django.db import models
from users.models import User
from core.utils import custom_id


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    status = (("draft", "Draft"), ("published", "Published"))
    id = models.CharField(primary_key=True, default=custom_id,
                          editable=False, max_length=16)
    title = models.CharField(max_length=100, blank=True, unique=True)
    excerpt = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to="posts", blank=True, null=True)
    _author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=status, default="draft")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    objects = models.Manager()
    published = PostManager()

    @property
    def author(self):
        try:
            return f"{self._author.first_name} {self._author.last_name}"
        except:
            return self._author

    @property
    def image_url(self):
        try:
            return f"http://127.0.0.1:8000{self.image.url}"
        except:
            return ""

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
