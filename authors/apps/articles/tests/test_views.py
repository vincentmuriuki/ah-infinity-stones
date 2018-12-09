from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from .test_config import MainTestConfig
from authors.apps.authentication.tests.test_setup import BaseSetUp
from authors.apps.articles.models import(
    Article, Tag
)


class CreateArticleTestCase(MainTestConfig):
    def setUp(self):
        self.article_data = {
            'title': 'The war storry',
            'author': 1,
            'tag': [1],
            'description': 'Love is blind',
            'body': 'I really loved war until...',
            'read_time': 3
        }

    def test_post_article(self):

        response = self.client.post(
            reverse('articles'), self.article_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_an_article(self):
        response = self.client.get(reverse('list', ))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_article(self):

        self.client.post(reverse('articles'), self.article_data, format="json")
        article = Article.objects.get()
        self.change_article = {'title': 'The love storry'}
        res = self.client.put(
            reverse('update', kwargs={'pk': article.id}),
            self.change_article,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_delete_article(self):
        self.client.post(reverse('articles'), self.article_data, format="json")
        article = Article.objects.get()
        response = self.client.delete(
            reverse('delete', kwargs={'pk': article.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


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

    # def test_user_can_update_comments(self):
    #     self.client.post(
    #         reverse('update_comment'), self.comment_data, format="json")
    #     comment = Comment.objects.get()
    #     self.change_article = {'title': 'The love storry'}
    #     res = self.client.put(
    #         reverse('update_comment', kwargs={'pk': comment.id}),
    #         self.change_article,
    #         format='json')

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)


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
            "api/users/login",
            self.login_data,
            format="json"
        )
        # Replace the dummy token with self.login_response.data["Token"]
        self.token = "eSknaojdIdlafesodoilkjIKLLKLJnjudalfdJndajfdaljfeESFdafjdalfjaofje"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        # Initialize tag data
        self.tag_data = {
            "tag": "Python"
        }

    def test_user_can_create_tag(self):
        """Test user can register new tags"""
        response = self.client.post(
            "api/articles/tags",
            self.tag_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_specific_tag(self):
        """Test api can return specific tag"""
        response = self.client.get(
            "api/articles/tags/1",
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_all_tag(self):
        """Test api can return all tags to enable easy filtering of articles"""
        response = self.client.get(
            "api/articles/tags",
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_specific_tag(self):
        """Test api can update a specific tag"""
        self.new_data = {"tag": "Love"}
        response = self.client.put(
            "api/articles/tags/1",
            self.new_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_specific_tag(self):
        """Test api can delete specific tag"""
        response = self.client.get(
            "api/articles/tags/1",
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_tag_an_article(self):
        """Test api can add tag to an article"""
        # add a new tag
        self.new_data = {"tag": "Marriage"}
        self.client.post(
            "api/articles/tags",
            self.new_data,
            format="json"
        )
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
            "api/articles/1",
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
