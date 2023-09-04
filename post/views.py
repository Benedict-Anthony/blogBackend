from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, CommentSerializer, PostViewSerializer, PostCRUDSerializer
from rest_framework import status
from rest_framework import permissions
from rest_framework import parsers

from .models import Post, Category
from .permissions import IsAuthorORPubisher, IsAuthor


class PostView(APIView):
    serializer_class = PostViewSerializer

    def get(self, request, slug=None):
        if slug:
            post = Post.published.get(slug=slug)
            serializer = self.serializer_class(post).data
            return Response(serializer)

        posts = Post.published.all()
        serializer = self.serializer_class(posts, many=True).data
        return Response(serializer)


class CategoryView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        category = Category.objects.all()
        serializer = self.serializer_class(category, many=True).data
        return Response(serializer)


class PostCRUDView(APIView):
    serializer_class = PostCRUDSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorORPubisher, IsAuthor]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def get(self, request, id=None):
        user = request.user
        if id:
            try:
                post = Post.objects.get(id=id)
                if user.is_publisher:
                    post = Post.objects.get(id=id, _author=request.user)

                serializer = self.serializer_class(post).data
                return Response(serializer)
            except Post.DoesNotExist:
                return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)
        posts = Post.objects.all()
        if not user.is_publisher:
            posts = posts.filter(_author=request.user)
        serializer = self.serializer_class(posts, many=True).data
        return Response(serializer)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(_author=request.user)
        return Response({"message": "success"}, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        try:
            query = Post.objects.get(id=id, _author=request.user)
            if request.user.id != query._author.id:
                return Response({"message": "you are not allowed to update this post"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(
                data=request.data, instance=query)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "update was succesfull"}, status=status.HTTP_202_ACCEPTED)
        except Post.DoesNotExist:
            return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        if request.user.is_publisher == False:
            return Response({"message": "you are not allowed to update this post"}, status=status.HTTP_403_FORBIDDEN)

        try:
            query = Post.objects.get(id=id)
            serializer = self.serializer_class(
                data=request.data, instance=query, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "update was succesfull"}, status=status.HTTP_202_ACCEPTED)
        except Post.DoesNotExist:
            return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            query = Post.objects.get(id=id)

            query.delete()
            return Response({"message": "post deleted"}, status=status.HTTP_202_ACCEPTED)
        except Post.DoesNotExist:
            return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)


class CommentView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "success!"}, status=status.HTTP_201_CREATED)
