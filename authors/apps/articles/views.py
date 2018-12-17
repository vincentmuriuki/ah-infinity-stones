from authors.apps.articles.models import Article, Comment
from rest_framework import generics
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, ListAPIView)


class ArticleCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({"Message": "article created successfully", "Data":
                         serializer.data}, status=status.HTTP_201_CREATED)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'art_slug'

    def update(self, request, art_slug, *args, **kwargs):
        article = Article.objects.get(art_slug=art_slug)
        serializer_data = request.data
        serializer = self.serializer_class(
            article, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
<<<<<<< HEAD
        return Response({"message": "article updated successfully", "Data":
                         serializer.data}, status=status.HTTP_200_OK)
=======
        return Response({"message": "article updated successfully", "Data": serializer.data}, status=status.HTTP_200_OK)
>>>>>>> Add slug functiopnality

    def delete(self, request, art_slug):
        queryset = Article.objects.get(art_slug=art_slug)
        queryset.delete()
<<<<<<< HEAD
        return Response({"message": "article deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
=======
        return Response({"message": "article deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
>>>>>>> Add slug functiopnality


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, slug):
        return Response(status=status.HTTP_200_OK)


<<<<<<< HEAD
=======
# class ArticleDeleteAPIView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


>>>>>>> Add slug functiopnality
class CommentCreateViewAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)
