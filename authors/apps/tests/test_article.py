from django.test import TestCase
# from ..models import Article
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class ViewTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.Article_data = {'title': 'The war storry'}

        self.response = self.client.post(
            reverse('article'),
            self.Article_data,
            format="json")
        

    def test_post_article(self):

        self.assertEqual(self.response.status_code,status.HTTP_201_CREATED)


    def test_api_can_get_an_article(self):
        article =  Article.objects.get()
        response = self.client.get(
            reverse("article", kwargs={"pk":article.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, article)
    
    def test_api_can_update_article(self):

        article = Article.objects.get()
        self.change_article = {'title': 'The love storry'}
        res = self.client.put(
            reverse('article',
            kwargs={'pk': article.id}),
            self.change_article,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.change_article)
    
    def test_api_can_delete_article(self):
        article = Article.objects.get()
        response = self.client.delete(
            reverse('article',
        kwargs={'pk':article.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    
    