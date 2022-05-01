# django rest framework
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

# django
from django.shortcuts import get_object_or_404
from django.db.models import Q

# core apps
from ..serializers import * 
from ..models import * 

# auth
from authentication.models import User

# contents models & view
from board.models import *
from event.models import *

from board.serializers import *
from event.serializers import *

from board.views import *
from event.views import *



CONTENTS_VIEW_DICT ={
    'post' : PostView(),
    'event' : EventView()
}



# 생각해보니 개귀찮네.. 
# 어차피 구분해서 할거면 걍 다 따로 해서 response날려주는게 나을듯

class WrapperListView(generics.GenericAPIView):
    serializer_class = WrapperSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        event의 경우 wrapper serialized도 필요하고
        event serialized도 필요함. 
        """

        kwargs = request.query_params

        
        if kwargs['content_type'] == "post":
            # event에는 post가 없어서 한번에 중복조건 걸면 에러 발생
            query_set = self.queryset.filter(
                Q(app_name__iexact = "post"))

            query_set = query_set.filter(
                Q(post__category__id__iexact =  kwargs['category_id'])
                ).order_by('-create_date')
            
            # serialize
            serializer = self.get_serializer(data=query_set, many = True)
            serializer.is_valid()
        
        elif kwargs['content_type'] == "event":

            if kwargs['view_type'] == 'table':
                query_set = self.queryset.filter(
                    Q(app_name__iexact = "event"))

                serializer = self.get_serializer(data=query_set, many = True)
                serializer.is_valid()

            else:
                query_set = Event.objects.all()

                serializer = EventSerializer(data= query_set, many = True)
                serializer.is_valid()
                
                
                # posting, 견적서 > 이건 table 형태로 볼거니까 기존대로
                # event에 해당하는 휴가, 업무나 이런건 어떻게 볼지에 따라 다름
                # 특히 업무는 table로 보고싶을 수 있음. (업무지시서가 추가된다면 특히 더)
                # view 방식을 하나 더 넣자. 

        

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        kwargs = request.query_params
        content_type = kwargs['content_type']        
        response = CONTENTS_VIEW_DICT[content_type].create(kwargs)
        
        # redirect 
        return response

class WrapperDetailView(generics.GenericAPIView):
    serializer_class = WrapperSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    # get
    def get(self, request, *args, **kwargs):
        print('wrapper detail')
        primary_key = request.parser_context['kwargs']['pk']
        kwargs = request.query_params
        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        contents = CONTENTS_VIEW_DICT[kwargs['content_type']].get(wrapper)
        
        serializer = WrapperSerializer(wrapper)

        contents['reply_set'] = serializer.data['reply_set']

        print(contents)
        
    
        return Response(contents, status= status.HTTP_200_OK)

class WrapperUpdateView(generics.GenericAPIView):
    serializer_class = WrapperSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    # get
    def post(self, request, *args, **kwargs):
        print('view update')
        primary_key = request.parser_context['kwargs']['pk']
        kwargs = request.query_params
        # 이걸 각 model에 알맞은 view로 연결
        # 여기서

        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        contents = CONTENTS_VIEW_DICT[kwargs['content_type']].update(wrapper, kwargs)
        
        # update

        
        # 여기서 replyset하고 comment set을 줘야 함
        serializer = WrapperSerializer(wrapper)
        contents['reply_set'] = serializer.data['reply_set']
        
    
        return Response(contents, status= status.HTTP_200_OK)


class WrapperDeleteView(generics.GenericAPIView):
    serializer_class = WrapperSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        primary_key = request.parser_context['kwargs']['pk']
        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        wrapper.delete()

        return Response({}, status= status.HTTP_200_OK)


