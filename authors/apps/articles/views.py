from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, ListAPIView)
from .serializers import ArticleSerializer, CommentSerializer
from authors.apps.articles.models import Article, Comment


class ArticleCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """ Method for creating an article """
        article = serializer.save(user=self.request.user)
        tags = Article.objects.get(pk=article.pk)
        for tag in article.tag:
            tags.tag.add(tag)
        return Response({"Message": "article created successfully", "Data":
                         serializer.data}, status=status.HTTP_201_CREATED)


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


class SearchArticleView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ArticleSerializer

    def get(self, request):
        search_params = request.query_params
        query_set = Article.objects.all()

        author = search_params.get('author', "")
        title = search_params.get('title', "")
        tag = search_params.get('tag', "")
        keywords = search_params.get('q', "")
        # filter based on the specific filter
        if author:
            query_set = query_set.filter(user__username=author)
        elif title:
            query_set = query_set.filter(title=title)
        elif tag:
            query_set = query_set.filter(tag__name=tag)
        elif keywords:
            # split the list of comma separated keywords
            words = str(keywords).split(',')
            final_queryset = ''
            for word in words:
                # filter titles based on the keyword(s) passed and
                # append them to final_queryset
                final_queryset = query_set.filter(title__icontains=word)
            query_set = final_queryset

        serializer = self.serializer_class(query_set, many=True)
        return_data = serializer.data
        if len(return_data) > 0:
            return Response({"Your search results": return_data},
                            status.HTTP_200_OK
                            )
        return Response({"Message": "Your search query did not match"
                         " anything in the database"})


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
