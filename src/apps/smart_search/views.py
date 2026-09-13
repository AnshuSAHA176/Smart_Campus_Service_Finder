from rest_framework.views import APIView
from django.contrib.gis.measure import Distance
from pgvector.django import CosineDistance
from .embbeding import create_embedding,embedding_model
from rest_framework.permissions import AllowAny
from .models import Place
from .serializer import PlaceSerializer
from rest_framework.response import Response
from .cetagory_classifyer import extract_search_intent

class SearchPlacesView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        message=request.data.get('message')
        if not message:
            return Response(
                {"error": "message is required"},
                status=400
            )
        user_qr_embedding=embedding_model(text=message)
        predict=extract_search_intent(message=message)
        if predict.category !='unknown':
            print(predict.category)
            related_places=Place.objects.filter(embedding__isnull=False,category=predict.category).annotate(distance=CosineDistance('embedding',user_qr_embedding)).order_by('distance')[:5]
        else:
            print(predict.category)
            related_places=Place.objects.filter(embedding__isnull=False).annotate(distance=CosineDistance('embedding',user_qr_embedding)).order_by('distance')[:5]
        serializer=PlaceSerializer(related_places,many=True)
        return Response(
            serializer.data
        )




