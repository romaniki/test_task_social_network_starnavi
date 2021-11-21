from django.conf.urls import url
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView

app_name = 'accounts-api'

urlpatterns = [
      path('api/register', RegisterAPIView.as_view()),
      path('api/login', LoginAPIView.as_view()),
]
