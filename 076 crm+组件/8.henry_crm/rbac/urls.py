"""luffy_permission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from rbac import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    # url(r'^index/$', views.index, name='index'),

    url(r'^menu/list/$', views.menu_list, name='menu_list'),
    url(r'^menu/add/$', views.menu_change, name='menu_add'),
    url(r'^menu/edit/(\d+)/$', views.menu_change, name='menu_edit'),
    url(r'^(menu|permission|role)/del/(\d+)/$', views.delete, name='del'),

    url(r'^permission/add/$', views.permission_change, name='permission_add'),
    url(r'^permission/edit/(\d+)/$', views.permission_change, name='permission_edit'),

    url(r'^role/list/$', views.role_list, name='role_list'),
    url(r'^role/add/$', views.role_change, name='role_add'),
    url(r'^role/edit/(\d+)/$', views.role_change, name='role_edit'),

    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),
    url(r'^distribute/permissions/$', views.distribute_permissions, name='distribute_permissions'),

]
