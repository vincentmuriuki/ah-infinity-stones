from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (ArticleCreateView, ArticleUpdateView, ArticleListAPIView,
                    ArticleDeleteAPIView, CommentCreateViewAPIView,
<<<<<<< HEAD
                    CommentListAPIView, CommentUpdateView)
=======
                    CommentUpdateView, CommentListAPIView)
>>>>>>> chore(article): test for article

urlpatterns = [
    path('articles', ArticleCreateView.as_view(), name='articles'),
    path('articles/<int:pk>', ArticleUpdateView.as_view(), name='update'),
    path('articles', ArticleListAPIView.as_view(), name='list'),
    path('delete/<int:pk>/', ArticleDeleteAPIView.as_view(), name='delete'),
    path('comment', CommentCreateViewAPIView.as_view(), name='comment'),
    path('comment', CommentListAPIView.as_view(), name='all_comments'),
    path(
<<<<<<< HEAD
        'comment/<int:pk>', CommentUpdateView.as_view(),
        name='update_comment'),
=======
        'comment/<int:pk>',
        CommentListAPIView.as_view(),
        name='comment_update'),
>>>>>>> chore(article): test for article
]
urlpatterns = format_suffix_patterns(urlpatterns)
