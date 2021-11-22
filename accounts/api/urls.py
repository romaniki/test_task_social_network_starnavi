from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, UserActivityAPIView


urlpatterns = [
      path('register', RegisterAPIView.as_view()),
      path('login', LoginAPIView.as_view()),
      path('logout', LogoutAPIView.as_view()),
      path('stat/<str:username>', UserActivityAPIView.as_view()),
]
