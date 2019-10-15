from django.conf.urls import url

from app01 import views

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UserView.as_view(), name='user'),
    url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name='dj'),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
]
