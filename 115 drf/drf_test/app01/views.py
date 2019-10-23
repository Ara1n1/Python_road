# Create your views here.
import json

from django.http import JsonResponse, HttpResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication, BasicAuthentication


class MyAuth():
    
    def authenticate(self, request):
        token = request.GET.get('token')
        if token:
            return True, True

        raise AuthenticationFailed('error')
    
    def authenticate_header(self, request):
        pass


class Login(APIView):
    authentication_classes = [MyAuth, ]

    def post(self, request, *args, **kwargs):
        return HttpResponse('ok')
