from django.urls import path
from .views import LoginView,RegisterView
from rest_framework_simplejwt.views import TokenRefreshView,TokenBlacklistView

urlpatterns = [
    path('login/',LoginView.as_view(),name= 'login'),
    path('register/',RegisterView.as_view(),name= 'register'),
    path('refresh/',TokenRefreshView.as_view(),name='for geting new access token'),
    path('logout/',TokenBlacklistView.as_view(),name="for invalidate the jwt token")
]