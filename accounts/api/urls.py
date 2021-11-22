from django.conf.urls import url
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView

app_name = 'accounts-api'

urlpatterns = [
      path('register', RegisterAPIView.as_view()),
      path('login', LoginAPIView.as_view()),
      path('user', UserAPIView.as_view()),
      path('logout', LogoutAPIView.as_view()),
]
