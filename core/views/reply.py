# django rest framework
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

# django
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

# core apps
from ..serializers import * 
from ..models import * 

# auth
from authentication.models import User

# contents models & view
from board.models import *
from board.views import *



# 생각해보니 개귀찮네.. 
# 어차피 구분해서 할거면 걍 다 따로 해서 response날려주는게 나을듯


class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        wrapper = get_object_or_404(Wrapper, pk =  request.query_params['wrapper_id'])
        serializer = WrapperSerializer(wrapper)
        reply_set = serializer.data['reply_set']      
        # reply를 주면 됨 
        return Response({'reply_set' : reply_set} ,status=status.HTTP_200_OK)

    def create(self, request):
        kwargs = request.query_params   
        wrapper = get_object_or_404(Wrapper, pk = kwargs['wrapper_id'])
        user = get_object_or_404(User, pk = kwargs['user_id'] )
        reply = Reply(wrapper = wrapper, author = user, content = kwargs['reply'])
        reply.save()
        reply = self.serializer_class(reply).data        
        return Response(reply ,status=status.HTTP_200_OK)

    def update(self, request):
        kwargs = request.query_params
        reply = get_object_or_404(Reply, pk = request.parser_context['kwargs']['pk'])
        reply.content = kwargs['content']
        reply.modify_date = timezone.now()
        reply.save()
        return Response({}, status = status.HTTP_200_OK)


    def delete(self, request):
        # 로직 수정
        # 그냥 아무것도 반환하지 말고 front에서만 지우자
        pk = request.parser_context['kwargs']['pk']
        reply = get_object_or_404(Reply, pk = pk)
        wrapper = reply.wrapper
        reply.delete()
        serializer = WrapperSerializer(wrapper)
        reply_set = serializer.data['reply_set']
        
        return Response({'reply_set' : reply_set}, status = status.HTTP_200_OK)

    


