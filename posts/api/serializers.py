from rest_framework import serializers
from posts.models import Post, Like
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['user', 'post', 'like', 'timestamp']
