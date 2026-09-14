from django.urls import path
from .views import ShortstPathView


urlpatterns=[
    path('',ShortstPathView.as_view(),name='test')
]