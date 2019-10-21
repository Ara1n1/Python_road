from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.

class Course(models.Model):
    """普通课程"""
    title = models.CharField(max_length=32)
    # 仅用于反向查找
    price_policy_list = GenericRelation('PricePolicy')


class DegreeCourse(models.Model):
    """学位课程"""
    title = models.CharField(max_length=32)
    price_policy_list = GenericRelation('PricePolicy')


class PricePolicy(models.Model):
    price = models.IntegerField()
    period = models.IntegerField()
    content_type = models.ForeignKey(ContentType, verbose_name='关联表名称')
    object_id = models.IntegerField(verbose_name='关联表数据ID')
    # 快速实现 content_type 操作
    content_obj = GenericForeignKey('content_type', 'object_id')
