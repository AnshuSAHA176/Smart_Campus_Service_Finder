from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import User
from rest_framework.permissions import AllowAny
from .serializer import RegisterSerializer,LoginSerializer
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        return Response (
            {
            "access":str(access_token),
            "refresh":str(refresh_token)

        }
        )

