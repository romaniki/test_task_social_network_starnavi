import jwt, datetime

from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer


class RegisterAPIView(APIView):

    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)


class LoginAPIView(APIView):
    
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

        return response


class UserAPIView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get("jwt")
        
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.get(id = payload.get("id"))
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': "You have been logged out."
        }
    
        return response
