from django.shortcuts import HttpResponse
from django.urls import reverse
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView


# Create your views here.
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