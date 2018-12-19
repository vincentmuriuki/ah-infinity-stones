import jwt

from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .test_config import MainTestConfig
from ..models import User
from authors.apps.authentication.tests.test_setup import BaseSetUp
from authors.apps.articles.models import (Article)


class SetUp(TestCase):
    """This class sets up test data"""

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
        self.filter_url = reverse('articles:search')


class CreateArticleTestCase(SetUp):

    def test_post_article(self):

        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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


class ArticleTagsTestCase(SetUp):
    """This class defines the Article Tags api test quiz"""

    def test_user_can_tag_an_article(self):
        """Test user can register new tags"""
        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tag'], self.article_data.get("tag"))

    def test_view_article_tags(self):
        """Test user can be able to view tags on a given article"""
        slug = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        ).data["art_slug"]
        response = self.client.get(
            self.article_url+"/{}".format(slug),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tag"], self.article_data.get("tag"))


class ArticleRatingTestCase(ArticleTagsTestCase):
    """This class defines the api to article rating test case"""

    def setUp(self):
        """Set or initialize the test data"""
        self.rating = {"article": 1, "author": 1, "rating": 5}

    def test_user_can_rate_an_article(self):
        """Test user can rate articles"""
        # add article
        self.article = {
            "title": "The mighty king",
            "author": 1,
            "tag": [1],
            "description": "Killed a lion with a sword",
            "body": "The JUJU king has done it again...",
            "read_time": 4
        }
        self.client.post("api/articles/", self.article, format="json")
        # Rate article
        response = self.client.post(
            "api/articles/ratings", self.rating, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get average ratings average rating for their articles
        response = self.client.post(
            "api/articles/user_ratings/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ Add the following code when ratings feature is implemented
            self.assertEqual(response.data['ratings'], 5)
        """


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


class ArticleSearchTest(SetUp):
    def test_user_can_filter_article_by_author(self):
        """ Test user is able to filter articles by author name"""
        # post one article
        self.client.post(self.article_url, self.article_data, format="json")
        self.article_data_2 = {
            'title': 'How to train your mind',
            'author': 1,
            'tag': ['philosophy'],
            'description': 'How can your mind train itself?',
            'body': 'Its actually possible, your mind is not you'
                    'so basically its you training the mind...',
            'read_time': 3
        }
        author = self.user['user']['username']
        # post a second article
        self.client.post(self.article_url, self.article_data, format="json")
        response = self.client.get(
            self.filter_url + '?author={}'.format(author), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_search_article(self):
        """ Test user can search articles by keywords"""
        self.client.post(self.article_url, self.article_data, format="json")
        self.article_data_2 = {
            'title': 'How to train your mind',
            'author': 1,
            'tag': ['philosophy'],
            'description': 'How can your mind train itself?',
            'body': 'Its actually possible, your mind is not you'
                    'so basically its you training the mind...',
            'read_time': 3
        }
        # post a second article
        self.client.post(self.article_url, self.article_data, format="json")
        response = self.client.get(self.filter_url + '?q=mind', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
