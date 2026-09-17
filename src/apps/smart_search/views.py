from rest_framework.views import APIView
from django.contrib.gis.db.models.functions import Distance
from pgvector.django import CosineDistance
from .embbeding import create_embedding,embedding_model
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .models import Place
from rest_framework import generics
from rest_framework.response import Response
from .cetagory_classifyer import extract_search_intent
from django.contrib.gis.geos import Point
from .serializer import PlaceSerializer,CurdSerializer
from rest_framework import pagination

class SearchPlacesView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        message = request.data.get("message")
        lng = request.data.get("longitude")
        lat = request.data.get("latitude")

        if not message:
            return Response(
                {"error": "message is required"},
                status=400
            )

        try:
            lng = float(lng)
            lat = float(lat)
        except (TypeError, ValueError):
            return Response(
                {"error": "latitude and longitude must be numbers"},
                status=400
            )

        if not (-90 <= lat <= 90):
            return Response(
                {"error": "Invalid latitude"},
                status=400
            )

        if not (-180 <= lng <= 180):
            return Response(
                {"error": "Invalid longitude"},
                status=400
            )

        user_point = Point(
            lng,
            lat,
            srid=4326
        )
        
        if not message:
            return Response(
                {"error": "message is required"},
                status=400
            )
        user_qr_embedding=embedding_model(text=message)

       

        related_places=(
                Place.objects.
                            filter(embedding__isnull=False).

                            annotate(distance=CosineDistance('embedding',user_qr_embedding)).
                            order_by('distance')[:20]
                            )
        related_places = related_places.annotate(
                geo_distance=Distance(
                    "location",
                    user_point
                )
            )
        result = []
        for place in related_places:
            semantic_score = 1 - place.distance

            distance_in_km=place.geo_distance.km

            geo_score= 1 / (1+distance_in_km)

            final_score=(
                0.7 * semantic_score+
                0.3 * geo_score
            )

            result.append(
                {
        "place": place,
        "semantic_score": semantic_score,
        "geo_score": geo_score,
        "final_score": final_score,
    }
            )


        result.sort(
            key=lambda x : x['final_score'],
            reverse=True
        )
        results = result[:5]
       
        data = [ {
                "id":item['place'].id,
                "name":item['place'].name,
                "description": item['place'].description,
                "category":item['place'].category,
                "semantic_score": item["semantic_score"],
                "geo_score": item["geo_score"],
                "final_score": item["final_score"],
                "distance":item['place'].geo_distance.m,
            }
            for item in results
            ]
    

        return Response(
            data
        )





class PlacePopulateView(generics.ListCreateAPIView):
    pagination_class=pagination.LimitOffsetPagination

    permission_classes=[IsAdminUser]

    queryset  = Place.objects.all()

    serializer_class = PlaceSerializer

class PlaceCurdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Place.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class=CurdSerializer



