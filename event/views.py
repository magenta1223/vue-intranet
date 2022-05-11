from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, viewsets

import json
from django.db.models import Q


from .serializers import * 
from .models import * 


from authentication.models import User
from core.models import Wrapper
from core.serializers import WrapperSerializer
from datetime import datetime, timedelta, timezone


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, kwargs):
        if kwargs['view_type'] == 'table':
            query_set = self.queryset.filter(
            Q(app_name__iexact = "event"))

            serializer = WrapperSerializer(data=query_set, many = True)
            serializer.is_valid()

            return Response(serializer.data)

        else:
            # query_set = Event.objects.all()
                
            query_set = self.queryset.filter(
                Q(app_name__iexact = "event")).filter(
                #private event가 아니거나
                Q(event__group__is_private = False) |
                # 내가 포함된 이벤트거나
                Q(event__group__user__id = kwargs['user_id']) |
                Q(event__relatedPeople__id__icontains = kwargs['user_id'])
                )


            print(query_set)


            serializer = WrapperSerializer(data= query_set, many = True)
            serializer.is_valid()

            user = get_object_or_404(User, pk = kwargs['user_id'])

            eventgroups = EventGroup.objects.all().filter(
                Q(user = user) | 
                Q(is_private = False)
            )
            eventgroups = EventGroupSerializer(data = eventgroups, many = True)
            eventgroups.is_valid()
            return Response({'data' : serializer.data, 'eventgroups' : eventgroups.data},  status= status.HTTP_200_OK)
            
    def create(self, kwargs):
        user = get_object_or_404(User, pk = kwargs['user_id'])
        eventgroup = get_object_or_404(EventGroup, pk = kwargs['event_group_id'])
                
        event = Event(
            start = kwargs['start'],
            end = kwargs['end'],
            author = user,
            group = eventgroup,
            title = kwargs['title'],
            description = kwargs['description']
            )
        event.save()

        if not kwargs['is_private']:
            # relatedPeople fields are many-to-many
            users= User.objects.all().filter(Q(id__in = kwargs['attendees']))
            event.relatedPeople.add(*users)
            event.save()
        wrapper = Wrapper(
            author = user,
            event = event,
            title = kwargs['title'],
            app_name = "event"
            )
        wrapper.save()
        wrapper = WrapperSerializer(wrapper)


        return wrapper.data

    def update(self, wrapper, kwargs):
        # update
        event = wrapper.event
        event.start = kwargs['start']
        event.end = kwargs['end']
        event.relatedPeople.clear()
        #users= User.objects.all().filter(Q(id__in = kwargs['attendees']))
        #event.relatedPeople.add(*users)
        event.group = get_object_or_404(EventGroup, pk = kwargs['event_group_id'])
        event.title = kwargs['title']
        event.description = kwargs['description']
        event.save()
        # serialize
        event = self.serializer_class(event).data
        event['model'] = 'event'
        return event 


class EventGroupViewSet(viewsets.ModelViewSet):
    serializer_class = EventGroupSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, kwargs):
        user = get_object_or_404(User, pk = kwargs['user_id'])
        eventgroup = EventGroup(
            type = kwargs['type'],
            name = kwargs['name'],
            color = kwargs['color'],
            is_private =  True if kwargs['is_private'] == 'true' else False,
            user = user,
            )
        eventgroup.save()
        wrapper = Wrapper(author = user, eventgroup = eventgroup, title = kwargs['name'])
        wrapper.save()
        eventgroup = EventGroupSerializer(eventgroup)


        return eventgroup.data

