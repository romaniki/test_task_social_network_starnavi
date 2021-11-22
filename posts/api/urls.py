from django.conf.urls import url
from django.urls import path, include
from .views import PostCreateAPIView, LikePostAPIView
from rest_framework import routers

app_name = 'posts-api'

router = routers.SimpleRouter()
router.register(r'like', LikePostAPIView)


urlpatterns = [
      path('create', PostCreateAPIView.as_view()),
      # path('like/<int:post>', LikePostAPIView.as_view()),
]

urlpatterns += router.urls
