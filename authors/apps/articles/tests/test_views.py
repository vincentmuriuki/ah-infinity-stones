import json
import jwt

from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from .test_config import MainTestConfig
from ..models import User
from authors.apps.authentication.tests.test_setup import BaseSetUp
from authors.apps.articles.models import (Article)


class CreateArticleTestCase(TestCase):
    def setUp(self):
        self.base = BaseSetUp()
        self.client = self.base.client
        self.user = {
            'user': {
                'username': 'remmy',
                'email': 'remmy@test.com',
                'password': '@Password123'
            }
        }
        self.article_data = {
            'art_slug': 'the-war-storry',
            'title': 'The war storry',
            'author': 1,
            'tag': ['js'],
            'description': 'Love is blind',
            'body': 'I really loved war until...',
            'read_time': 3
        }

        response = self.client.post(
            reverse('authentication:register'), self.user, format="json")
        decoded = jwt.decode(
            response.data['Token'], settings.SECRET_KEY, algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        user.is_active = True
        self.token = response.data['Token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        user.save()
        self.article_url = reverse('articles:articles')

    def test_post_article(self):

        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # self.assertIn(b'article created successfully',
        #   response.content)

    def test_user_can_get_an_article(self):
        response = self.client.get(self.article_url,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_article(self):
        self.client.post(self.article_url, self.article_data, format="json")
        article = Article.objects.get()
        self.change_article = {'title': 'The love storry'}
        response = self.client.put(
            reverse('articles:update', kwargs={'art_slug': article.art_slug}),
            self.change_article,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'article updated successfully',
                      response.content)

    def test_user_can_delete_article(self):
        self.client.post(self.article_url, self.article_data, format="json")
        article = Article.objects.get()
        response = self.client.delete(
            reverse('articles:update', kwargs={'art_slug': article.art_slug}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('article deleted successfully',
                      response.data['message'])


class CreateCommentTestCase(MainTestConfig):
    def setUp(self):
        self.comment_data = {'article': 1, 'user': 1, 'comment': 'Nice story '}

    def test_user_can_post_a_comment(self):
        response = self.client.post(
            reverse('comment'), self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_all_comments(self):
        response = self.client.get(reverse('all_comments', ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArticleTagsTestCase(TestCase):
    """This class defines the api for Tag CRUD methods"""

    def setUp(self):
        """"This method sets the test variables and test client"""
        self.base = BaseSetUp()
        self.client = self.base.client
        # Initialize login credentials
        self.login_data = {
            "username": "remmy@test.com",
            "password": "Password123"
        }
        # Declare login response
        self.login_response = self.client.post(
            "api/users/login", self.login_data, format="json")
        # Replace the dummy token with self.login_response.data["Token"]
        self.token = "eSknaojdIdlafesodoilkjIKLLKLJnjudalfdJndajfdaljfeESFdafjdalfjaofje"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_user_can_create_tag(self):
        """Test user can register new tags"""
        self.tag_data = {"tag": "Python"}
        response = self.client.post(
            "api/articles/tags", self.tag_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_specific_tag(self):
        """Test api can return specific tag"""
        response = self.client.get("api/articles/tags/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_all_tag(self):
        """Test api can return all tags to enable easy filtering of articles"""
        response = self.client.get("api/articles/tags", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_specific_tag(self):
        """Test api can update a specific tag"""
        self.new_data = {"tag": "Love"}
        response = self.client.put(
            "api/articles/tags/1", self.new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_specific_tag(self):
        """Test api can delete specific tag"""
        response = self.client.get("api/articles/tags/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_tag_an_article(self):
        """Test api can add tag to an article"""
        # add a new tag
        self.new_data = {"tag": "Marriage"}
        self.client.post("api/articles/tags", self.new_data, format="json")
        # add article
        self.article = {
            'title': 'The marriage story',
            'author': 1,
            'tag': [1],
            'description': 'Love is blind',
            'body': 'My wife was a criminal until she met this handsome guy.',
            'read_time': 5
        }
        # tag article
        self.article_data = {
            "tag": [2],
        }
        response = self.client.put(
            "api/articles/1", self.article_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArticleRatingTestCase(TestCase):
    """This class defines the api to article rating test case"""
    def setUp(self):
        self.base = BaseSetUp()
        self.client = self.base.client
        self.user_1 = {
            'user': {
                'username': 'remmy',
                'email': 'remmy@test.com',
                'password': '@Password123'
            }
        }
        self.user_2 = {
            'user': {
                'username': 'Ronny',
                'email': 'ronny@test.com',
                'password': '@Password123'
            }
        }
        self.user_3 = {
            'user': {
                'username': 'Mageh',
                'email': 'mageh@test.com',
                'password': '@Password123'
            }
        }
        self.rating_1 = {"rating": "2"}
        self.rating_2 = {"rating": "5"}
        
    def register_user(self, user):
        response = self.client.post(
            reverse('authentication:register'), user, format="json")
        decoded = jwt.decode(
            response.data['Token'], settings.SECRET_KEY, algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        user.is_active = True
        self.token = response.data['Token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        user.save()
    
    def post_article(self):
        """Register the author and post article"""
        # first register the author
        self.register_user(self.user_1)
        # add article
        self.article_url = reverse('articles:articles')
        self.article_data = {
            'art_slug': 'the-war-storry',
            'title': 'The war storry',
            'author': 1,
            'tag': ['js'],
            'description': 'Love is blind',
            'body': 'I really loved war until...',
            'read_time': 3
        }
        self.response_article_posted = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.rating_url = '/api/articles/' + \
                          self.response_article_posted.data['art_slug'] + \
                          '/rate'

    def test_author_cannot_rate_their_own_article(self):
        """Test author cannot rate his/her own article"""
        self.post_article()
        response_POST = self.client.post(self.rating_url, self.rating_1,
                                         format="json")
        self.assertEqual(response_POST.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_POST.data['message'], "You cannot rate " +
                         "your own article.")
        # Get all ratings for this article
        response_GET = self.client.get(self.rating_url)
        self.assertEqual(response_GET.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_GET.data), 0)

    def test_audience_can_rate_article(self):
        """Test audience (one) can rate an article"""
        self.post_article()
        self.register_user(self.user_2)
        # Rate article
        response_POST = self.client.post(self.rating_url, self.rating_1,
                                         format="json")
        response_GET = self.client.get(self.rating_url)
        self.assertEqual(response_POST.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_POST.data['message'], "Thank you for " +
                         "taking time to rate this article.")
        # Get all ratings for this article
        response_GET = self.client.get(self.rating_url)
        self.assertEqual(response_GET.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_GET.data), 1)

    def test_article_rating_average_updates(self):
        """Test user can rate articles"""
        # user_2 rates the article
        self.test_audience_can_rate_article()
        # register user 3
        self.register_user(self.user_3)
        # user 3 rates article
        response_POST = self.client.post(self.rating_url, self.rating_2,
                                         format="json")
        response_GET = self.client.get(self.rating_url)
        self.assertEqual(response_POST.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_POST.data['message'], "Thank you for " +
                         "taking time to rate this article.")
        # Get all ratings for this article
        response_GET = self.client.get(self.rating_url)
        self.assertEqual(response_GET.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_GET.data), 2)
        response_ARTICLE_DATA = self.client.get(self.article_url)
        self.assertEqual(response_ARTICLE_DATA.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ARTICLE_DATA.data[0]['rating_average'],
                         '3.50')
        

class ArticleLikeDisklikeTestCase(ArticleTagsTestCase):
    """This class defines the api test case to like or dislike articles"""

    def setUp(self):
        """Set or initialize the test data"""
        # add article
        self.article = {
            "title": "The killer disease",
            "author": 1,
            "tag": [1],
            "description": "HIV revisited",
            "body": "Handily did they love him until he was no more...",
            "read_time": 2
        }
        self.like = {"article": 1, "user": 1, "like": True}
        self.client.post("api/articles", self.article, format="json")
        response = self.client.post(
            "api/articles/likes", self.like, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleFavoriteTestCase(ArticleTagsTestCase):
    """This class defines the api test case to favorite articles"""

    def setUp(self):
        """Set or initialize the test data"""
        # add article
        self.article = {
            "title": "Life Hack Guide",
            "author": 1,
            "tag": [1],
            "description": "Discorer you life in 3 minutes.",
            "body": "Many people still do not to know what they value in life",
            "read_time": 3
        }
        self.favorite = {"article": 1, "user": 1, "favorite": True}
        self.client.post("api/articles", self.article, format="json")
        response = self.client.post(
            "api/articles/favorites", self.favorite, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
