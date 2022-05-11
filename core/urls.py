from .views import wrapper, landing, reply
from django.urls import include, path
from rest_framework import routers, urls  # router import

router = routers.DefaultRouter()  # DefaultRouter 설정
router.register('wrapper', wrapper.WrapperViewSet)  # ViewSet과 함께 user라는 router 등록
router.register('reply', reply.ReplyViewSet)  # ViewSet과 함께 user라는 router 등록

# list route
# url : /prefix/
# 'get': 'list' 'post': 'create'
# rapper에 method get으로 접근시 list 반환
# post로 접근 시 create 결과 반환 뭐 이런식임

# detail route

# url : /prefix/pk/
# 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy',



landing_view = landing.LandingView.as_view()

urlpatterns = [
    path('', include(router.urls)),
    path('landing/', landing_view, name = "landing"),
]