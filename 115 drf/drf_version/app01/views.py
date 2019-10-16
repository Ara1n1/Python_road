import json

from django.shortcuts import HttpResponse
from django.urls import reverse
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView

# Create your views here.
from app01 import models


class ParamVersion:

    def determine_version(self, request, *args, **kwargs):
        version = request.GET.get('version')
        return version


class UserView(APIView):
    # restful 可以自己拿到 版本号
    # 自定义
    # versioning_class = ParamVersion
    # 使用内置
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        # version = request.GET.get('version')
        # v = request.query_params.get('version')
        # print(version, v)

        # url 反向解析
        url = request.versioning_scheme.reverse(viewname='user', request=request)
        print(url, 'here')

        # 使用django 的url 反向解析
        user_url = reverse(viewname='user', kwargs={'version': 'v2'})
        print('user_url: ', user_url)
        return HttpResponse('用户列表')


class DjangoView(APIView):

    def post(self, request, *args, **kwargs):
        print(request._request)
        print(request.POST)
        print(request.body)
        return HttpResponse('ok')


from rest_framework.parsers import JSONParser, FormParser


class ParserView(APIView):
    parser_classes = [JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        # 获取解析后的结果
        print(request.POST)
        # print(request.body)
        print(request.data)
        return HttpResponse('ParserView')


"""序列化器"""

from rest_framework import serializers


class MySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32)


class RoleView(APIView):

    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()

        # 方式一
        # roles = roles.values()
        # print(type(roles), roles)
        # roles = json.dumps(list(roles), ensure_ascii=False)

        # 方式二,针对单个对象
        ser = MySerializer(instance=roles, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)


# class UserInfoSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     # choices 选项
#     user_type = serializers.CharField(source='get_user_type_display')
#     # 外键
#     group = serializers.CharField(source='group.title')
#     # 多对对关系
#     # role = serializers.CharField(source='role.all')
#     role = serializers.SerializerMethodField()
#
#     def get_role(self, row):
#         row_obj_list = row.role.all()
#         ret = []
#         for i in row_obj_list:
#             ret.append({'id': i.id, 'title': i.title})
#         return ret

"""继承 ModelSerializer """


class UserInfoSerializer(serializers.ModelSerializer):
    # group = serializers.CharField(source='group.title')
    # user_type = serializers.CharField(source='get_user_type_display')
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')

    class Meta:
        model = models.UserInfo
        fields = '__all__'
        depth = 1


class UserInfoView(APIView):

    def get(self, request, *args, **kwargs):
        userinfo = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=userinfo, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = '__all__'


class GroupView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        groups = models.UserGroup.objects.filter(pk=pk)
        ser = GroupSerializer(instance=groups, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
