from django.db import models

from codelieche.django.models.base import BaseModel


# Create your models here.
class Book(BaseModel):
  title = models.CharField(verbose_name="标题", max_length=128)
  author = models.CharField(verbose_name="作者", max_length=64, blank=True, null=True)
  price = models.DecimalField(verbose_name="价格", max_length=6, max_digits=4, blank=True, null=True, decimal_places=2)
  store = models.IntegerField(verbose_name="库存", blank=True, default=0)
  description = models.TextField(verbose_name="描述", blank=True, null=True)
  time_deleted = models.DateTimeField(verbose_name="删除时间", blank=True, null=True)

  class Meta:
    verbose_name = "书籍"
    verbose_name_plural = verbose_name
