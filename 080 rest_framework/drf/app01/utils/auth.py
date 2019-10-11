from rest_framework import exceptions

from app01 import models


class MyAuth:

    def authenticate(self, request):
        ret = {'code': 1000, 'msg': None, 'data': None}
        token = request.GET.get('token')
        print(token)
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token:
            ret['code'] = 1001
            ret['msg'] = '用户没有登录'
            raise exceptions.AuthenticationFailed(ret)
        # restful framework 内部会赋值给requst，供以后使用
        return token_obj.user, token_obj

    def authenticate_header(self, request):
        pass
