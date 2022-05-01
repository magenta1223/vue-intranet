
from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import
from django.contrib.auth import authenticate

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = '__all__'




class WrapperSerializer(serializers.ModelSerializer):
    #reply_set = serializers.StringRelatedField(many=True) # ReplySerializer(read_only = True, many = True)
    reply_set = ReplySerializer(many = True)

    class Meta:
        model = Wrapper
        fields = (
            'id',
            'author',
            'title',
            'create_date',
            'modify_date',
            'post',
            'event',
            'reply_set')

    