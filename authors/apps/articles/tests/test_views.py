from rest_framework import status
from django.urls import reverse
from .test_config import MainTestConfig
from authors.apps.articles.models import Article


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

    def test_api_can_get_an_article(self):
        response = self.client.get(reverse('list', ))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_update_article(self):

        self.client.post(reverse('articles'), self.article_data, format="json")
        article = Article.objects.get()
        self.change_article = {'title': 'The love storry'}
        res = self.client.put(
            reverse('update', kwargs={'pk': article.id}),
            self.change_article,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_article(self):
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

    def test_post_a_comment(self):
        response = self.client.post(
            reverse('comment'), self.comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
