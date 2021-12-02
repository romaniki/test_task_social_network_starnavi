import jwt
from datetime import datetime

from django.db.models import Count

from accounts.models import User

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import AuthenticationFailed

from .serializers import PostSerializer, LikeSerializer
from .signals import track_activity_signal
from posts.models import Post, Like


def get_current_user(token):
    """Get current user object generated JWT token"""
    if not token:
        raise AuthenticationFailed("Unauthenticated")
    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")
    return User.objects.get(id=payload.get("id"))


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        token = self.request.COOKIES.get("jwt")
        track_activity_signal.send(sender=get_current_user(token), timestamp=datetime.now())
        return serializer.save(author=get_current_user(token))


class LikePostAPIView(UpdateModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = 'post'

    def get_object(self):
        token = self.request.COOKIES.get("jwt")
        obj, _ = Like.objects.get_or_create(user=get_current_user(token), post=Post.objects.get(id=self.kwargs['post']))

        # Keep track of the last like and unlike activities
        track_activity_signal.send(sender=get_current_user(token), timestamp=datetime.now())

        return obj


class LikeAnalyticsAPIView(APIView):
    """Analytics about how many likes was made aggregated by day."""

    def get(self, request):
        
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        likes = Like.objects\
            .filter(timestamp__range=[date_from, date_to], like=True)\
            .values('timestamp__date')\
            .annotate(**{'total':Count('timestamp__date')})\

        response = Response()
        response.data = {
            'likes': likes
        }
        return response
