# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


from codelieche.django.utils import Cryptography


class BaseModel(models.Model):
    """
    基础Model类
    添加了deleted字段, 覆写了save方法
    """
    delete_tasks = ()  # 需要执行的删除函数的任务（函数列表）
    SECRET_FIELDS = ()  # 需要加密的字段
    delete_update_fields = ()  # 删除的时候需要自动修改的字段
    delete_time_field_name = None  # 删除的时候自动记录时间
    # delete_time_field_name = "time_deleted"  # 删除的时候自动记录时间

    # 字段：删除、添加时间
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True, null=True)

    @staticmethod
    def strftime(fmt='%Y%m%d%H%M%S'):
        """
        格式化当前的时间戳，删除资源的时候会用到
        """
        return timezone.datetime.now().strftime(fmt)

    def set_decrypt_value(self):
        # 加密存储的字段
        if self.SECRET_FIELDS and isinstance(self.SECRET_FIELDS, (list, tuple)):
            p = Cryptography()

            # 自己配置SECRET_FIELDS, BaseModel中默认是[]
            for i in self.SECRET_FIELDS:
                value = getattr(self, i)
                if i and value:
                    # 判断是否是加密的
                    success, _ = p.check_can_decrypt(value)
                    if not success:
                        setattr(self, i, p.encrypt(text=value))
            # 对需要加密的字段加密完毕

    def get_decrypt_value(self, field: str) -> str:
        """
        获取解密后的值
        """
        value = getattr(self, field)
        if value:
            p = Cryptography()
            success, de_p = p.check_can_decrypt(value=value)
            if success:
                return de_p
            else:
                return value

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 调用设置加密字段的方法
        self.set_decrypt_value()
        # 调用父类的save方法
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_relative_object_by_model(self, model, args=None, value=None, many=False, field="pk"):
        """
        通过model获取关系的对象
        多值还是单值，自行判断
        :param model: 类，必须是django的类
        :param args: 过滤条件，必须是dict
        :param value: 过滤检索的值，有可能是列表
        :param many: 是否是多值
        :param field: 过滤的字段，默认是pk
        :return:
        """
        # 1. 构造检索的数据
        # field自己处理，比如：id__in，等
        if args and isinstance(args, dict):
            data = args
        elif value:
            data = {field: value}
        else:
            raise ValueError("args或者value必须传递一个")

        # 2. 判断model是否正确
        if not issubclass(model, models.Model):
            raise ValueError("传入的model必须是django.db.Modeel的子类")

        # 3. 开始过滤数据
        if many:
            queryset = model.objects.filter(**data)
            return queryset
        else:
            # 这个直接用get是有可能报错的（比如根据一条字段，得到了2条数据），这个传入端去处理
            obj = model.objects.get(**data)
            return obj

    def get_relative_object_by_content_type(self, app_label, model, args=None, value=None, many=False, field="pk"):
        """
        根据content_type获取到对象
        :param app_label: app的名字
        :param model: 类，必须是django的类的名称
        :param args: 过滤条件，必须是dict
        :param value: 过滤检索的值，有可能是列表
        :param many: 是否是多值
        :param field: 过滤的字段，默认是pk
        :return:
        """
        # 1. 根据app_label和model获取到Model
        ct = ContentType.objects.filter(app_label=app_label, model=model).first()
        if not ct:
            return None
        model_cls = ct.model_class()

        # 2. 调用get_relative_object_by_model获取对象
        return self.get_relative_object_by_model(model=model_cls, args=args, value=value, many=many, field=field)


    def do_delete_update_field(self):
        """
        当对象删除的时候，需要自动修改的字段，加入 _del_的标识
        """
        if isinstance(self.delete_update_fields, (tuple, list)):
            for field in self.delete_update_fields:
                value = getattr(self, field)
                if value and isinstance(value, str) and value.find('_del_') < 0:
                    value_new = "{}_del_{}".format(value, self.strftime())
                    setattr(self, field, value_new)
                    try:
                        self.save(update_fields=(field,))
                    except Exception as e:
                        # 比如长度超过了，就会报错
                        print('自动修改字段报错：{}'.format(str(e)))
                    # print("需要修改的字段：{}，值为:{}".format(field, value))

    def do_delete_action(self):
        """
        重要系统，数据尽量只标记删除，不要做物理删除
        当我们删除对象的时候，可能需要执行额外的任务
        比如：修改某个字段(把某个字段加个时间戳)、删除额外的关联数据、比如关联了我的数据也需要删除掉
        """
        if self.deleted:
            # 1. 判断是否已经删除，如果已经是标记删除的了，那我们就直接返回
            return
        else:
            # 2. 遍历需要执行的删除的任务，我们对其进行删除
            if isinstance(self.delete_tasks, (list, tuple)):
                for i in self.delete_tasks:
                    # 别循环调用自己了
                    if i and hasattr(self, i) and i != 'do_delete_action':
                        task_func = getattr(self, i)
                        # 判断一下这个是否是函数
                        if hasattr(task_func, '__call__'):
                            # 我们执行调用函数
                            task_func()
                        else:
                            print('{}不是可调用的函数', i)
            # 3. 修改删除的字段：在delete_update_fields中会调用save方法
            if self.delete_update_fields:
                self.do_delete_update_field()

            # 4. 修改deleted字段
            self.deleted = True
            update_fields = ['deleted']

            # 5. 修改删除时间
            if self.delete_time_field_name:
                try:
                    # 判断是否有这个字段, 如果没这个字段是会报错的
                    self._meta.get_field(self.delete_time_field_name)
                    setattr(self, self.delete_time_field_name, timezone.datetime.now(tz=timezone.utc))
                    update_fields.append(self.delete_time_field_name)
                except Exception as e:
                    pass
            self.save(update_fields=update_fields)

    def delete(self, using=None, keep_parents=False):
        # 1. 判断是否有do_delete_action的属性，且是可调用的
        if hasattr(self, "do_delete_action") and callable(self.do_delete_action):
            self.do_delete_action()
        else:
            # 如果没有就调用父类的删除方法，注意这里是调用models.Model的delete方法
            super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        # 抽象类
        abstract = True
