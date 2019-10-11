import json

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework import exceptions
from rest_framework.views import APIView

from app01 import models


class MyAuthentication(object):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用于认证失败')
        return ('henry', None)

    def authenticate_header(self, request):
        pass


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


"""认证相关"""


def md5(user):
    import hashlib, time
    m = hashlib.md5(bytes(user, encoding='utf8'))
    m.update(bytes(str(time.time()), encoding='utf8'))
    return m.hexdigest()


class AuthView(APIView):

    def post(self, request):
        ret = {'code': 1000, 'msg': None}
        user = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        obj = models.UserInfo.objects.filter(username=user, password=pwd)

        if not obj:
            ret['code'] = 1001
            ret['msg'] = '用户名或密码错误'
        else:
            # 为登录用户创建 token
            token = md5(user)
            # token 存在更新，不存在更新
            user_id = obj.first().id
            models.UserToken.objects.update_or_create(user_id=user_id, defaults={"token": token})
            ret['token'] = token
        return JsonResponse(ret)
