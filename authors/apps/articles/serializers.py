from rest_framework import serializers
from authors.apps.articles.models import (
    Article, User, Tag, Comment, LikeDislike)
from taggit_serializer.serializers import TagListSerializerField
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer that converts querysets to json data"""
    user = serializers.ReadOnlyField(source='user.username')
    tag = TagListSerializerField()

    class Meta:

        model = Article
        fields = (
            "id",
            "art_slug",
            "title",
            "description",
            "body",
            "read_time",
            "tag",
            "user",
            "created_at",
            "updated_at")


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]


class LikeSerializer(serializers.ModelSerializer):
    """ Serialize json to model and model to json"""

    class Meta:
        model = LikeDislike
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=LikeDislike.objects.all(),
                fields=('article', 'user')
            )
        ]
