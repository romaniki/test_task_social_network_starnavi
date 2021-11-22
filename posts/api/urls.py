from django.urls import path
from .views import PostCreateAPIView, LikePostAPIView, LikeAnalyticsAPIView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'post/like', LikePostAPIView)

urlpatterns = [
      path('post/create', PostCreateAPIView.as_view()),
      path('analytics/', LikeAnalyticsAPIView.as_view()),
]

urlpatterns += router.urls
