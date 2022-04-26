from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )





urlpatterns = [
    path('admin/', admin.site.urls), # admin path 지정
    #user.api의 모든 url 정보를 받아오는 path 설정 (include)

    path("", include("authentication.urls")),

    path('api/', include('core.urls')),



]