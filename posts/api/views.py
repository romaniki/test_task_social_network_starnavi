import jwt

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import PostSerializer, LikeSerializer
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
        return serializer.save(author=get_current_user(token))


class LikePostAPIView(UpdateModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = 'post'

    def get_object(self):
        token = self.request.COOKIES.get("jwt")
        obj, _ = Like.objects.get_or_create(user=get_current_user(token), post=Post.objects.get(id=self.kwargs['post']))
        return obj



# Like.objects.filter(like_post=post.id).aggregate(Count('pk'))
