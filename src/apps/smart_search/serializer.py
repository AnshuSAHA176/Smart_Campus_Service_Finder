from rest_framework.serializers import ModelSerializer
from .models import Place




class PlaceSerializer(ModelSerializer):
    class Meta:
        model=Place
        fields=[
            'name',
            'description',
            'category',
            'location',
              ]


