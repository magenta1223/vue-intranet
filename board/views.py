from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
import json

from .serializers import * 
from .models import * 

from authentication.models import *
from core.models import *
from core.serializers import *
from django.db.models import Q

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Wrapper.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, kwargs):
        
        query_set = self.queryset.filter(
            Q(app_name__iexact = "post")).filter(
            Q(post__category__id__iexact =  kwargs['category_id'])
            ).order_by('-create_date')
            
        # serialize
        serializer = WrapperSerializer(data=query_set, many = True)
        serializer.is_valid()
        return Response(serializer.data)
        
    def create(self, kwargs):
        user = get_object_or_404(User, pk = kwargs['user_id'])
        category = get_object_or_404(Category, pk = kwargs['category_id'])
        
        post = Post(
            author = user,
            title = kwargs['title'],
            content = kwargs['content'],
            category = category)
        post.save()

        wrapper = Wrapper(
            author = user,
            post = post,
            title = kwargs['title'],
            app_name = "post")
        wrapper.save() 
        post = PostSerializer(post)
        return post.data

    def retrieve(self, wrapper):
        post = self.serializer_class(wrapper.post).data
        post['model'] = 'post'
        return post #Response(post, status=status.HTTP_200_OK)

    def update(self, wrapper, kwargs):
        post = wrapper.post
        post.title = kwargs['title']
        post.content = kwargs['content']
        post.category = get_object_or_404(Category, pk = kwargs['category_id'])
        post.save()
        
        # title, content, category
        post = self.serializer_class(post).data
        post['model'] = 'post'




class CategoryView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    # get에서 
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.queryset)
        return self.list(serializer, *args, **kwargs)