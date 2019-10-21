import json

from django.shortcuts import HttpResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView

# Create your views here.
from app01 import models
from app01.utils.serializers import PageSerializer

"""url携带参数"""


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
    parser_classes = [FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        # 获取解析后的结果
        print(request.POST)
        # print(request.data)
        # print(request.body)
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


#
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


"""验证功能"""


class XxValidator(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, value, *args, **kwargs):
        if not value.startswith(self.base):
            message = 'This Filed must start with %s!' % self.base
            raise serializers.ValidationError(message)


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required': '标题字段不能为空'}, validators=[XxValidator('henry')])


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        msg = '数据提交成功'
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            msg = ser.errors
            print(msg)
        return HttpResponse('%s' % msg)


"""分页"""
from rest_framework.pagination import CursorPagination, PageNumberPagination

# class Page1View(APIView):
#     def get(self, request, *args, **kwargs):
#         roles = models.Role.objects.all()
#         # 实例化 PageNumberPagination 类
#         pg = PageNumberPagination()
#         page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
#         print(page_roles)
#         ser = PageSerializer(instance=page_roles, many=True)
#         return Response(ser.data)

"""自定义分页器"""


# class MyPagination(PageNumberPagination):
#     # 每页显示个数
#     page_size = 2
#     # 通过page指定哪一页
#     page_query_param = 'page'
#     # 指定每页显示条数
#     page_size_query_param = 'size'
#     # 指定每页最大的数据量
#     max_page_size = 5


# class MyPagination(LimitOffsetPagination):
#     default_limit = 2
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'
#     max_limit = 6


class MyPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'
    page_size_query_param = 'size'
    max_page_size = 6


class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        # 实例化 PageNumberPagination 类
        # pg = PageNumberPagination()
        # pg = LimitOffsetPagination()
        # pg = CursorPagination()
        pg = MyPagination()
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(page_roles)
        ser = PageSerializer(instance=page_roles, many=True)

        # return Response(ser.data)
        return pg.get_paginated_response(ser.data)


"""视图"""

# from rest_framework.generics import GenericAPIView
# class ViewView(GenericAPIView):
#     queryset = models.Role.objects.all()
#     serializer_class = PageSerializer
#     pagination_class = PageNumberPagination
#
#     def get(self, reqeust, *args, **kwargs):
#         # 获取数据
#         roles = self.get_queryset()
#         # 获取分页的数据
#         page_roles = self.paginate_queryset(roles)
#         # 序列化
#         ser = self.get_serializer(instance=page_roles, many=True)
#
#         return Response(ser.data)


# from rest_framework.viewsets import GenericViewSet
#
#
# class ViewView(GenericViewSet):
#     queryset = models.Role.objects.all()
#     serializer_class = PageSerializer
#     pagination_class = PageNumberPagination
#
#     def list(self, reqeust, *args, **kwargs):
#         # 获取数据
#         roles = self.get_queryset()
#         # 获取分页的数据
#         page_roles = self.paginate_queryset(roles)
#         # 序列化
#         ser = self.get_serializer(instance=page_roles, many=True)
#
#         return Response(ser.data)
#
#     def xxx(self, reqeust, *args, **kwargs):
#         pass


# from rest_framework.viewsets import GenericViewSet
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
#
#
# class ViewView(ListModelMixin, CreateModelMixin, GenericViewSet):
#     queryset = models.Role.objects.all()
#     serializer_class = PageSerializer
#     pagination_class = PageNumberPagination


from rest_framework.viewsets import ModelViewSet


class ViewView(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PageSerializer
    pagination_class = PageNumberPagination


"""渲染器"""


class TestView(APIView):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        pg = PageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(page_roles)
        ser = PageSerializer(instance=page_roles, many=True)
        return Response(ser.data)
