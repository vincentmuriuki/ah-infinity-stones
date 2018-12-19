from authors.apps.articles.models import Article, Comment, ArticleRating
from rest_framework import generics
from django.db.models import Avg
from .serializers import ArticleSerializer, CommentSerializer,\
                         ArticleRatingSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, ListAPIView)
from rest_framework.permissions import IsAuthenticated


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
        return Response({"message": "article updated successfully", "Data":
                         serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, art_slug):
        queryset = Article.objects.get(art_slug=art_slug)
        queryset.delete()
        return Response({"message": "article deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, slug):
        return Response(status=status.HTTP_200_OK)


class ArticleRatingAPIView(generics.ListCreateAPIView):
    """
    get:
    Retrieve all article ratings
    post:
    Create a new article rating
    """
    permission_classes = (IsAuthenticated,)
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleRatingSerializer

    def post(self, request, art_slug):
        """
        Creates an article rating
        :params HttpRequest: A post request with article rating data sent by
        clients to create a new article rating.
        :return: Returns a successfully created article rating
        """
        # Retrieve article rating data from the request object and convert it
        # to a kwargs object
        # get user data at this point
        try:
            article = Article.objects.get(art_slug=art_slug)
        except Exception:
            response = {"message": "That article does not exist"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article.user_id == request.user.id:
            data = {
                "message": "You cannot rate your own article."
            }
            return Response(data, status.HTTP_403_FORBIDDEN)

        article_rating = {
            'art_slug': art_slug,
            'username': request.user.username,
            'rating': request.data.get('rating', None),
        }
        # pass article data to the serializer class, check whether the data is
        # valid and if valid, save it.
        serializer = self.serializer_class(data=article_rating)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Save the average article rating to the Article model
        q = ArticleRating.objects.filter(art_slug=article.art_slug).aggregate(
            Avg('rating'))
        article.rating_average = q['rating__avg']
        article.save(update_fields=['rating_average'])
        data = {"message": "Thank you for taking time to rate this article."}

        return Response(data, status.HTTP_201_CREATED)


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
