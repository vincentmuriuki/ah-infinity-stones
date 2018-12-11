from django.urls import path, re_path

from .views import LoginAPIView, RegistrationAPIView, \
    UserRetrieveUpdateAPIView, SocialAuthAPIView, ActivationView,\
    PasswordResetBymailAPIView
from rest_framework import views

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('login/oauth/', SocialAuthAPIView.as_view(), name="social_auth"),
<<<<<<< HEAD
    re_path(r'^user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/\
    (?P<token>[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+))/',
=======
    re_path(r'^user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+))/',
>>>>>>> Refactor tests
            ActivationView.as_view(), name='activate'),
    path('socialAuth/', SocialAuthAPIView.as_view()),
    path('user/password-reset/', PasswordResetBymailAPIView.as_view()),
    path('', views.index),
    path('done', views.done),
    path('reset', views.reset),
    path('thanks', views.thanks),
]
