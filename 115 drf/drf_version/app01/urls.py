from django.conf.urls import url, include
from rest_framework import routers

from app01 import views

router = routers.DefaultRouter()
router.register(r'xxx', views.ViewView)
router.register(r'yyy', views.ViewView)

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/user/$', views.UserView.as_view(), name='user'),
    url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name='dj'),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/role/$', views.RoleView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),

    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', views.GroupView.as_view(), name='gp'),
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view(), name='ugp'),

    # 分页
    url(r'^(?P<version>[v1|v2]+)/page1/$', views.Page1View.as_view()),
    # 视图
    # # url(r'^(?P<version>[v1|v2]+)/view/$', views.ViewView.as_view()),
    # url(r'^(?P<version>[v1|v2]+)/view/$', views.ViewView.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^(?P<version>[v1|v2]+)/view/(?P<format>\w+)/$', views.ViewView.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^(?P<version>[v1|v2]+)/view/(?P<pk>\d+)/$', views.ViewView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    # url(r'^(?P<version>[v1|v2]+)/view/(?P<pk>\d+)/(?P<format>\w+)/$', views.ViewView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),

    # 路由配置
    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),

    # 渲染器 
    url(r'^(?P<version>[v1|v2]+)/test/$', views.TestView.as_view()),
]
