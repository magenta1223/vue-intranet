from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import * 
from .models import * 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics 

from rest_framework import mixins
import json


from authentication.models import *
from core.models import *



class PostView( mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, wrapper):
        # https://www.codegrepper.com/code-examples/python/customise+the+django+rest+api+view
        post = self.serializer_class(wrapper.post).data
        post['model'] = 'post'
        
        return post #Response(post, status=status.HTTP_200_OK)

    def create(self, kwargs):
        
        user = get_object_or_404(User, pk = kwargs['user_id'])
        category = get_object_or_404(Category, pk = kwargs['category_id'])
        
        post = Post(author = user, title = kwargs['title'], content = kwargs['content'], category = category)
        post.save()

        wrapper = Wrapper(author = user, post = post, title = kwargs['title'], app_name = "post")
        print(wrapper.title)
        wrapper.save() 

        return Response(status=status.HTTP_200_OK)


    def update(self, wrapper, kwargs):
        # https://www.codegrepper.com/code-examples/python/customise+the+django+rest+api+view

        # 일단 수정 후 serialize
        post = wrapper.post
        post.title = kwargs['title']
        post.content = kwargs['content']
        post.category = get_object_or_404(Category, pk = kwargs['category_id'])
        post.save()
        
        # title, content, category

        post = self.serializer_class(wrapper.post).data
        post['model'] = 'post'

        return post #Response(post, status=status.HTTP_200_OK)


class CategoryView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    # get에서 
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.queryset)
        return self.list(serializer, *args, **kwargs)