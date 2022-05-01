from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics 

import json


from .serializers import * 
from .models import * 


from authentication.models import *
from core.models import *





class EventView(generics.GenericAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, wrapper):
        # https://www.codegrepper.com/code-examples/python/customise+the+django+rest+api+view
        event = self.serializer_class(wrapper.event).data
        event['model'] = 'event'

        # id: '1', # 있음
        # calendarId: '0', # 없음. 필요
        # title: 'TOAST UI Calendar Study', # 없음. 필요 
        # category: 'time', # 이건 computed attribute로 넣자
        # dueDateClass: '', # ? 
        # start: today.toISOString(), # 있음
        # end: getDate('hours', today, 3, '+').toISOString() # 있음 
        
        return event #Response(post, status=status.HTTP_200_OK)

    def create(self, kwargs):
        
        user = get_object_or_404(User, pk = kwargs['user_id'])
        eventgroup = get_object_or_404(EventGroup, pk = kwargs['event_group_id'])

        event = Event(
            start = kwargs['start'],
            end = kwargs['end'],
            author = user,
            group = eventgroup,
            title = kwargs['title']
            )
        event.save()
        
        # relatedPeople fields are many-to-many
        for rp in kwargs['relatedPeople']:
            user = get_object_or_404(User, pk = rp)
            event.relatedPeople.add(user)
        event.save()

        wrapper = Wrapper(author = user, event = event, title = kwargs['title'])
        wrapper.save() 

        return Response(status=status.HTTP_200_OK)


    def update(self, wrapper, request):
        # https://www.codegrepper.com/code-examples/python/customise+the+django+rest+api+view

        # update
        event = wrapper.event
        query_params = request.query_params

        event.start = query_params['start']
        event.end = query_params['end']
        event.color = query_params['color']
        
        event.relatedPeople.clear()

        for rp in query_params['relatedPeople']:
            user = get_object_or_404(User, pk = rp)
            event.relatedPeople.add(user)

        event.save()
        
        # serialize

        event = self.serializer_class(wrapper.event).data
        event['model'] = 'event'

        return event #Response(post, status=status.HTTP_200_OK)

