
from rest_framework import serializers

from .models import * # 선언한 모델 import
from django.contrib.auth import authenticate

from board.serializers import PostSerializer # serializer import
from event.serializers import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = '__all__'




class WrapperSerializer(serializers.ModelSerializer):
    # One to Many Field
    reply_set = ReplySerializer(many = True)
    # One to One Field
    post = PostSerializer()
    event = EventSerializer()
    eventgroup = EventGroupSerializer()

    class Meta:
        model = Wrapper
        fields = "__all__"
        # fields = (
        #     'id',
        #     'author',
        #     'title',
        #     'create_date',
        #     'modify_date',
        #     'post',
        #     'event',
        #     'reply_set')

    