from django.db import models

from codelieche.django.models.base import BaseModel


# Create your models here.
class Book(BaseModel):
  title = models.CharField(verbose_name="标题", max_length=128)
  author = models.CharField(verbose_name="作者", max_length=64, blank=True, null=True)
  store = models.IntegerField(verbose_name="库存", blank=True, default=0)
  time_deleted = models.DateTimeField(verbose_name="删除时间", blank=True, null=True)

  class Meta:
    verbose_name = "书籍"
    verbose_name_plural = verbose_name
