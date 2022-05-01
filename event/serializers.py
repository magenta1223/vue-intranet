from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import
from django.contrib.auth import authenticate

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



    