from django.shortcuts import HttpResponse


# Create your views here.

def test(reqeust):
    return HttpResponse('ok')
