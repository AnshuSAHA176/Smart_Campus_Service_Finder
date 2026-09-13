from rest_framework import serializers
from .models import Place
from django.contrib.gis.geos import Point
from .embbeding import create_embedding


class PlaceSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(
        write_only=True,
        min_value=-90,
        max_value=90
    )

    longitude = serializers.FloatField(
        write_only=True,
        min_value=-180,
        max_value=180
    )
    class Meta:
        model=Place
        fields=[
            'pk',
            'name',
            'description',
            'category',
            'location',
            'latitude',
            'longitude',
           

            


              ]
        extra_kwargs = {
            
            'location': {
                            'read_only': True, 
                            
                        },
            }

    
    def create(self, validated_data):

        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')

        validated_data['location'] = Point(
            longitude,
            latitude,
            srid=4326
        )

        validated_data['embedding'] = create_embedding(
            title=validated_data['name'],
            description=validated_data['description'],
            category=validated_data['category']
        )

        return Place.objects.create(**validated_data)
        


class CurdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"