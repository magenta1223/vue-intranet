from .views import *
from django.urls import include, path
from rest_framework import routers, urls  # router import

post_list = PostView.as_view()

urlpatterns = [
    path('post/', post_list, name='wrapper'),
    #path('wrapper/<int:pk>', wrapper_detail, name='wrapper_detail'),
]