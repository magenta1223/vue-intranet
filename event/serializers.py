from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import
from django.contrib.auth import authenticate




class EventGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGroup
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    group = EventGroupSerializer()
    class Meta:
        model = Event
        fields = '__all__'

class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'