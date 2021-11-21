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
        
        except ObjectDoesNotExist:
            return Response(data={"detail": "User not found"})
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        return Response({"You are successfully logged in."})
