from rest_framework import serializers
from authors.apps.articles.models import Article, User, Tag, Comment
from taggit_serializer.serializers import (TagListSerializerField)


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
    share_urls = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Article
        fields = ("art_slug", "title", "description", "body", "read_time",
                  "tag", "user", "share_urls", "created_at", "updated_at")

    def get_share_urls(self, instance):
        """
        Populates share_urls with google, facebook, and twitter share urls.
        """
        request = self.context.get('request')
        return instance.get_share_uri(request=request)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]
