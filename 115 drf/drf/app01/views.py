import json

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework import exceptions
from rest_framework.views import APIView

from app01 import models

"""测试使用"""


class MyAuthentication:

    def authenticate(self, request):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用于认证失败')
        return ('henry', None)

    def authenticate_header(self, request):
        pass


class DemoView(APIView):
    # authentication_classes = [MyAuthentication, ]
    authentication_classes = []

    def get(self, reqeust):
        return HttpResponse('DemoView get')

    def post(self, request):
        return HttpResponse('DemoView post')

    def put(self, request):
        return HttpResponse('DemoView put')


class Test(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request):
        print(request)
        return HttpResponse(json.dumps({'status': '200 ok', 'name': 'henry'}))

    def post(self, request):
        return HttpResponse('POST')

    def put(self, request):
        return HttpResponse('put')

    def delete(self, request):
        return HttpResponse('delete')


"""用户登录类"""


class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    # throttle_classes = [MyThrottle, ]

    def post(self, request):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            print(user, pwd)
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为登录用户创建 token
            token = self.md5(user)
            # token 存在更新，不存在更新
            models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
            ret['token'] = token
        except Exception as e:
            pass

        return JsonResponse(ret)

    """用户认证相关"""

    def md5(self, user):
        import hashlib, time
        m = hashlib.md5(bytes(user, encoding='utf8'))
        m.update(bytes(str(time.time()), encoding='utf8'))
        return m.hexdigest()


data = {
    1: {
        'oid': 1,
        'name': 'henry',
    },
    2: {
        'oid': 2,
        'name': 'echo',
    },
    3: {
        'oid': 3,
        'name': 'dean',
    },

}

"""权限相关"""


class OrderView(APIView):
    # permission_classes = [MyPermission, ]

    def get(self, request):

        ret = {'code': 1000, 'msg': None, 'data': None}

        print(request.user, request.auth)
        try:
            ret['data'] = data
        except Exception as e:
            pass
        return JsonResponse(ret)
