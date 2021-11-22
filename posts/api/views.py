import jwt
from datetime import datetime

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
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        return User.objects.get(id = payload.get("id"))


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
        
        track_activity_signal.send(sender=get_current_user(token), timestamp=datetime.now())
        
        return obj


class LikeAnalyticsAPIView(APIView):

    def get(self, request):
        
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        aggregated_by_date = {}

        likes = Like.objects.filter(timestamp__range=[date_from, date_to], like=True)

        for like in likes:
            date = like.timestamp.date().strftime("%d/%m/%Y")
            if date not in aggregated_by_date:
                aggregated_by_date[date] = 1
            else:
                aggregated_by_date[date] += 1

        response = Response()
        response.data = {
            'likes': aggregated_by_date
        }
        return response
