from django.urls import path
from .views import SearchPlacesView


urlpatterns=[
    path('search/',SearchPlacesView.as_view(),name='search')
]