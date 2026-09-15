from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import User
from rest_framework.permissions import AllowAny
from .serializer import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class 