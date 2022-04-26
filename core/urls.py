from .views import wrapper, landing, reply
from django.urls import include, path
from rest_framework import routers, urls  # router import

wrapper_list = wrapper.WrapperListView.as_view()
wrapper_detail = wrapper.WrapperDetailView.as_view()
landing_view = landing.LandingView.as_view()

reply_create = reply.ReplyView.as_view()

urlpatterns = [
    path('landing/', landing_view, name = "landing"),
    path('wrapper/', wrapper_list, name='wrapper'),
    path('wrapper/<int:pk>', wrapper_detail, name='wrapper_detail'),
    path('reply/', reply_create, name='reply_create'),
]