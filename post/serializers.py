from rest_framework import serializers
from .models import Post, Category, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "name", "content"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post

        fields = ["id", "title", "excerpt", "content", "author",
                  "category",  "image_url", "created_at", "slug", "comments"]


class PostCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "excerpt", "content",
                  "category", "status", "image", "slug"]
