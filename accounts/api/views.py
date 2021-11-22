import datetime
import jwt

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .serializers import UserSerializer
from .signals import track_login_signal


class RegisterAPIView(APIView):

    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPIView(APIView):
    """Implement login with token authentication (JWT)"""

    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect password")

            payload = {
                "id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat": datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

        except ObjectDoesNotExist:
            return Response(data={"detail": "User not found"})

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

        # Track the last login of the user with django signals
        track_login_signal.send(sender=user, timestamp=datetime.datetime.now())

        return response


class LogoutAPIView(APIView):

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': "You have been logged out."
        }

        return response


class UserActivityAPIView(APIView):
    """Show when user was login last time and when he made a last request to the service."""

    def get(self, request, *args, **kwargs):

        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)

        return Response(
            {
                'last login': user.last_login,
                'last activity': user.last_activity
            })
