from django.http import HttpResponse

from app01 import models


# Create your views here.
def test(request):
    # obj = models.DegreeCourse.objects.filter(title='python全栈').first()
    # models.PricePolicy.objects.create(price=9.9, period=30, content_obj=obj)
    #
    # obj = models.DegreeCourse.objects.filter(title='python全栈').first()
    # models.PricePolicy.objects.create(price=19.9, period=60, content_obj=obj)
    #
    # obj = models.DegreeCourse.objects.filter(title='python全栈').first()
    # models.PricePolicy.objects.create(price=29.9, period=90, content_obj=obj)

    course = models.DegreeCourse.objects.filter(id=1).first()
    # 获取所有课程对象
    price_poicy = course.price_policy_list.all()
    print(price_poicy)
    for i in price_poicy:
        print(i.id, i.price, i.period, i.object_id, i.content_type_id)

    return HttpResponse('ok')
