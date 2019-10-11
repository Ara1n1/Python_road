from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = 'xxxx'
    def has_permission(self, request, view):

        # 返回 True 则有权访问
        return False