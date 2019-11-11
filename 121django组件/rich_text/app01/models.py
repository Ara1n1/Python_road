from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.

class Test(models.Model):
    content = RichTextUploadingField(verbose_name='article info')
