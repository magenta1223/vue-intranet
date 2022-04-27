# django rest framework
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, generics, status
from rest_framework import generics 
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



CONTENTS_VIEW_DICT ={
    'post' : PostView()
}

MODEL_DICT ={
    'post' : Post
}


# 생각해보니 개귀찮네.. 
# 어차피 구분해서 할거면 걍 다 따로 해서 response날려주는게 나을듯

class ReplyCreateView(generics.GenericAPIView):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        kwargs = request.query_params
        wrapper_id = kwargs['wrapper_id']        
        user_id = kwargs['user_id']        
        
        wrapper = get_object_or_404(Wrapper, pk = wrapper_id)
        user = get_object_or_404(User, pk = user_id)

        reply = Reply(wrapper = wrapper, author = user, content = kwargs['reply'])
        reply.save()

        reply = self.serializer_class(reply).data        
        # reply를 주면 됨 

        
        return Response(reply ,status=status.HTTP_200_OK)

class ReplyListView(generics.GenericAPIView):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        kwargs = request.query_params
        wrapper = get_object_or_404(Wrapper, pk = kwargs['wrapper_id'])
        serializer = WrapperSerializer(wrapper)
        reply_set = serializer.data['reply_set']      
        # reply를 주면 됨 

        
        return Response({'reply_set' : reply_set} ,status=status.HTTP_200_OK)


class ReplyUpdateView(generics.GenericAPIView):
    
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        kwargs = request.query_params
        
        reply = get_object_or_404(Reply, pk = pk)

        reply.content = kwargs['content']
        reply.modify_date = timezone.now()

        reply.save()
        # content 수정하고 수정시각 logging하면됨
        return Response({}, status = status.HTTP_200_OK)



class ReplyDeleteView(generics.GenericAPIView):
    
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        reply = get_object_or_404(Reply, pk = pk)
        wrapper = reply.wrapper
        reply.delete()
        
        serializer = WrapperSerializer(wrapper)
        reply_set = serializer.data['reply_set']

        
        # content 수정하고 수정시각 logging하면됨
        return Response({'reply_set' : reply_set}, status = status.HTTP_200_OK)



    


