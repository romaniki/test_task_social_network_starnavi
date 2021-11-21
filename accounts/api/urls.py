from django.conf.urls import url
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView

app_name = 'accounts-api'

urlpatterns = [
      path('api/register', RegisterAPIView.as_view()),
      path('api/login', LoginAPIView.as_view()),
      path('api/user', UserAPIView.as_view()),
      path('api/logout', LogoutAPIView.as_view()),
]
