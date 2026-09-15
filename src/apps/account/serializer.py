from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
        
            'email',
            
            'password'

        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):

        user=User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email = attrs['email'], password = attrs ['password'])
        if user == None:

            raise serializers.ValidationError("wrong email and password")



        attrs['user'] = user

        return user


