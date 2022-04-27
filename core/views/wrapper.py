# django rest framework
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, generics, status
from rest_framework import generics 
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
from board.views import *



CONTENTS_VIEW_DICT ={
    'post' : PostView()
}

MODEL_DICT ={
    'post' : Post
}


# 생각해보니 개귀찮네.. 
# 어차피 구분해서 할거면 걍 다 따로 해서 response날려주는게 나을듯

class WrapperListView(generics.GenericAPIView):
    serializer_class = WrapperSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.query_params.get('content_type', False):
            if request.query_params['content_type'] == "post":
                query_set = self.queryset.filter(Q(
                    post__category__id__iexact =  request.query_params['category_id']
                )).order_by('-create_date')

        else:
            query_set = self.queryset
        serializer = self.get_serializer(data=query_set, many = True)
        serializer.is_valid()

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
        
        # 이걸 각 model에 알맞은 view로 연결
        # 여기서

        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        view_class = CONTENTS_VIEW_DICT[request.query_params['content_type']]
        contents = view_class.get(wrapper)
        
        # 여기서 replyset하고 comment set을 줘야 함
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
        
        # 이걸 각 model에 알맞은 view로 연결
        # 여기서

        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        contents = CONTENTS_VIEW_DICT[request.query_params['content_type']].update(wrapper, request)
        
        # update

        
        # 여기서 replyset하고 comment set을 줘야 함
        serializer = WrapperSerializer(wrapper)
        contents['reply_set'] = serializer.data['reply_set']
        
    
        return Response(contents, status= status.HTTP_200_OK)



    


