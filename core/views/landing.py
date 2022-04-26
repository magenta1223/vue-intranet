# django rest framework
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from rest_framework import generics 
from rest_framework.response import Response

# django
from django.shortcuts import get_object_or_404

# core apps
from ..serializers import * 
from ..models import * 

# contents models & view
from board.models import *
from board.views import *


class LandingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    # get에서 
    def get(self, request, *args, **kwargs):
        # all categories

        categories = CategorySerializer(Category.objects.all(), many = True)
        
        return Response({
            "categories" : categories.data
        })


