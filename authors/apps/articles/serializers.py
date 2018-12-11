from rest_framework import serializers
from authors.apps.articles.models import Article, User, Tag, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class ArticleSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True, many=True)

    class Meta:

        model = Article
        fields = ("author", "tag", "description", "body", "read_time")


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]

        
