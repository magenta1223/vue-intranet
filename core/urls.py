from .views import wrapper, landing, reply
from django.urls import include, path
from rest_framework import routers, urls  # router import


landing_view = landing.LandingView.as_view()

wrapper_list = wrapper.WrapperListView.as_view()
wrapper_detail = wrapper.WrapperDetailView.as_view()
wrapper_update = wrapper.WrapperUpdateView.as_view()


reply_create = reply.ReplyCreateView.as_view()
reply_list = reply.ReplyListView.as_view()
reply_update = reply.ReplyUpdateView.as_view()
reply_delete = reply.ReplyDeleteView.as_view()

urlpatterns = [
    path('landing/', landing_view, name = "landing"),
    path('wrapper/', wrapper_list, name='wrapper'),
    path('wrapper/<int:pk>', wrapper_detail, name='wrapper_detail'),
    path('wrapper/update/<int:pk>', wrapper_update, name='wrapper_update'),

    path('reply/', reply_create, name='reply_create'),
    path('reply/list/', reply_list, name='reply_list'),
    path('reply/<int:pk>', reply_update, name='reply_update'),
    path('reply/delete/<int:pk>', reply_delete, name='reply_delete'),

]