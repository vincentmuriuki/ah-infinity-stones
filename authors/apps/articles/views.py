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
        """ Method for creating an article """
        text = serializer.validated_data['body']
        read_time = self.article_read_time(text)
        serializer.save(user=self.request.user, read_time=read_time)
        return Response({"Message": "article created successfully", "Data":
                         serializer.data}, status=status.HTTP_201_CREATED)

    def article_read_time(self, text):
        """Method that calculates article read time"""
        wpm = 200
        total_words = len(text.split())

        read_time = total_words / wpm

        return int(round(read_time))


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'art_slug'

    def update(self, request, art_slug, *args, **kwargs):
        """ Method for updating an article """
        article = Article.objects.get(art_slug=art_slug)
        serializer_data = request.data
        serializer = self.serializer_class(
            article, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "article updated successfully", "Data":
                         serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, art_slug):
        """ Method for deleting an article """
        queryset = Article.objects.get(art_slug=art_slug)
        queryset.delete()
        return Response({"message": "article deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, slug):
        """ Method for getting all articles """
        return Response(status=status.HTTP_200_OK)


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
