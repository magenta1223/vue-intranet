# django rest framework
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
    'post' : PostViewSet(),
    'event' : EventViewSet(),
    'eventgroup' : EventGroupViewSet()
}


class WrapperViewSet(viewsets.ModelViewSet):
    serializer_class = WrapperSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        kwargs = request.query_params
        return CONTENTS_VIEW_DICT[kwargs['content_type']].list(kwargs)

    def create(self, request):
        kwargs = request.query_params
        content = CONTENTS_VIEW_DICT[kwargs['content_type']].create(kwargs)
        return Response(content, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        wrapper = get_object_or_404(Wrapper, pk = request.parser_context['kwargs']['pk'])
        return Response(WrapperSerializer(wrapper).data)

    def update(self, request, pk=None):
        primary_key = request.parser_context['kwargs']['pk']
        kwargs = request.query_params
        # 이걸 각 model에 알맞은 view로 연결

        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        CONTENTS_VIEW_DICT[kwargs['content_type']].update(wrapper, kwargs)

        return Response(WrapperSerializer(wrapper).data, status= status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        primary_key = request.parser_context['kwargs']['pk']
        wrapper = get_object_or_404(Wrapper, pk = primary_key)
        wrapper.delete()

        return Response({}, status= status.HTTP_200_OK)