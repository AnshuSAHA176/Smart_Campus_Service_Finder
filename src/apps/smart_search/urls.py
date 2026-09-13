from django.urls import path
from .views import SearchPlacesView,PlacePopulateView,PlaceCurdView


urlpatterns = [
    path('search/', SearchPlacesView.as_view(), name='place-search'),
    path('places/', PlacePopulateView.as_view(), name='place-list-create'),
    path('places/<int:pk>/', PlaceCurdView.as_view(), name='place-detail'),
]
