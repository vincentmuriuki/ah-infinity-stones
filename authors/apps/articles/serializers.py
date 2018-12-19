from rest_framework import serializers
from authors.apps.articles.models import Article, User, Tag, Comment,\
                                         ArticleRating
from taggit_serializer.serializers import (TagListSerializerField)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tag = TagListSerializerField()

    class Meta:

        model = Article
        fields = ("id", "art_slug", "title", "description", "body", "read_time",
                  "tag", "user", "created_at", "updated_at", "rating_average")


class ArticleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleRating
        """
        Declare all fields we need to be returned from ArticleRating model
        """
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ArticleRatingSerializer, self).__init__(*args, **kwargs)

        # Override the error_messages of each field with a custom error message
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['null'] = field_error_messages['blank'] \
                = field_error_messages['required'] \
                = 'Please fill in the {}'.format(field)

    def update(self, instance, validated_data):
        """
        Method for updating an existing ArticleRating object
        """
        
        instance.art_slug = validated_data.get('art_slug', instance.art_slug)
        instance.username = validated_data.get('username', instance.username)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Method for creating an ArticleRating object
        It checks if a user has made a rating for an article. If yes it calls
        the update method. If not, it creates a new ArticleRating object.
        """
        article_rating_object, created = ArticleRating.objects.get_or_create(
            art_slug=validated_data.get('art_slug'),
            username=validated_data.get('username'),
            defaults={'rating': validated_data.get('rating', None)}, )
        
        if not created:
            self.update(instance=article_rating_object,
                        validated_data=validated_data)

        return article_rating_object


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]
