from django.db import models


# Create your models here.
class Info(models.Model):
    username = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)





