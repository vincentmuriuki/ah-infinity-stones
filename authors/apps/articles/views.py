from authors.apps.articles.models import Article, Comment
from rest_framework import generics
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (RetrieveUpdateAPIView, ListAPIView,
                                     DestroyAPIView)


class ArticleCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleUpdateView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def update(self, request, pk):
        return Response(status=status.HTTP_200_OK)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)


class ArticleDeleteAPIView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def delete(self, request, pk):
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateViewAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdateView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)
