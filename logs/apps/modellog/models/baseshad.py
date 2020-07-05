# -*- coding:utf-8 -*-

from django.db import models


class Object:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class BaseShard:
    """
    模型分表
    """

    _shard_db_models = {}

    def __new__(cls, *args, **kwargs):
        shard_key = kwargs.pop("shard_key", "")
        model_name = cls.__name__

        if shard_key != "":
            model_name += "_%s" % shard_key
        else:
            model_name = "{}__default".format(model_name)

        model_class = cls._shard_db_models.get(model_name)

        if model_class is not None:
            return model_class

        # 开始构造分片后的model
        attrs = dict()

        attrs.update(cls.__dict__)

        if "objects" in attrs:
            attrs["objects"] = attrs["objects"].__class__()

        # Set table name with shard_key
        meta = Object(**cls.Meta.__dict__)

        # 如果shard_key为空就用默认的
        if shard_key:
            meta.db_table = "{}_{}".format(meta.db_table, shard_key)

        attrs["Meta"] = meta
        # attrs["new"] = classmethod(_mode_new)

        # Create model class dynamically
        model_class = type(model_name, tuple([models.Model] + list(cls.__bases__[1:])), attrs)
        cls._shard_db_models[model_name] = model_class
        return model_class


class Book(BaseShard, models.Model):
    """
    分片测试Model
    """

    name = models.CharField(verbose_name="名称", blank=True, max_length=128)
    author = models.CharField(verbose_name="作者", blank=True, max_length=128)

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name


class ShardBook(BaseShard):
    """
    分片测试Model
    """

    name = models.CharField(verbose_name="名称", blank=True, max_length=128)
    author = models.CharField(verbose_name="作者", blank=True, max_length=128)

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name
        db_table = "modellog_book"
