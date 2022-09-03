# -*- coding:utf-8 -*-
from rest_framework.decorators import action
from rest_framework.response import Response


class BatchActionMixin:
    """
    批量操作的Mixin
    比如：批量添加操作的时候，批量修改的时候
    """

    # 一般我们只批量添加
    batch_actions = ("batch", "create",)
    # 批量操作对象的主键字段名
    batch_action_pk_field_name = 'id'

    def get_serializer(self, *args, **kwargs):
        # 判断是否是批量的时候：如果传递的是数组，那么就可以批量创建
        # 比如：批量创建对象
        if self.action in self.batch_actions and isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
            # kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

    @action(methods=["PUT", "PATCH", "DELETE", "POST"], description="批量操作", detail=False)
    def batch(self, request, pk=None):
        # 1. 批量创建
        if request.method == "POST":
            # 这个是批量创建操作
            return self.create(request=request)

        # 2. 批量更新
        elif request.method in ["PUT", "PATCH"]:
            # 这个是批量更新操作，我们需要判断一下传递的值中是否传递了id
            # 批量更新就不是使用self.update这个了，update里面有个self.get_object()没法知道获取哪个instance
            data = request.data
            if isinstance(data, list):
                # 3-1：检查每个数据
                index = 0
                for item in data:
                    index += 1
                    # 每一项数据需要是个dict类型，且必须包含主键(batch_action_pk_field_name)，且值不可为空
                    if not (
                            isinstance(item, dict) and self.batch_action_pk_field_name in item and
                            item[self.batch_action_pk_field_name]
                    ):
                        message = "第{}项不含有{}的字段值，不可更新:{}".format(index, self.batch_action_pk_field_name, item)
                        results = {
                            "status": False,
                            "message": message
                        }
                        return Response(results, status=400)

                # 3-2：开始批量更新: 这个接口，暂时自动记录修改日志的功能会失效，后续可优化
                serializer_class = self.get_serializer_class()
                results = []
                context = self.get_serializer_context()
                # 是否是局部更新
                partial = request.method == 'PATCH'

                # 遍历传递的列表，逐个更新对象
                for item in data:
                    # 获取到实例
                    queryset = self.get_queryset()
                    params = {self.batch_action_pk_field_name: item[self.batch_action_pk_field_name]}
                    # 利用queryset来获取是为了防止跨权限操作了
                    instance = queryset.filter(**params).first()
                    if instance:
                        # 利用序列化类更新对象
                        serializer = serializer_class(instance, data=item, partial=partial, context=context)
                        # print('serializer:', serializer)
                        if serializer.is_valid():
                            # 保存更新
                            serializer.save()
                            # 把更新后的新序列化对象，加入到结果列表中
                            results.append(serializer.data)
                        else:
                            # 验证错误的就返回错误信息
                            results.append(serializer.errors)
                    else:
                        msg = "实例未找到"
                        results.append(msg)
                # 遍历结束，返回结果
                return Response(data=results)
            else:
                results = {
                    "status": False,
                    "message": "批量操作，请传递列表数据"
                }
                return Response(results, status=400)

        # 3. 批量删除操作
        elif request.method == "DELETE":
            # 小心没传递query_params就全部删除了，
            if request.query_params and self.batch_action_pk_field_name in request.query_params:
                values = request.query_params.get(self.batch_action_pk_field_name)
                if values:
                    values = values.split(',')
                    # 再次过滤
                    params = {
                        '{}__in'.format(self.batch_action_pk_field_name): values,
                    }
                    try:
                        queryset = self.get_queryset().filter(**params)
                        # print(queryset)
                        # 调用各个对象的delete方法，不是要批量删除，因为批量删除不会触发我们Model自定义的delete task
                        for item in queryset:
                            if hasattr(self, 'perform_destroy'):
                                # 如果继承了modellog的mixin那么删除的时候会记录操作日志
                                self.perform_destroy(item)
                            else:
                                item.delete()
                    except Exception as e:
                        print("批量删除获取对象出现异常：{}".format(str(e)))
                # 返回响应
                return Response(status=204)
            else:
                # 如果未传递query_params的值，我们报错提示
                results = {
                    "status": False,
                    "message": "未传递{}的值".format(self.batch_action_pk_field_name)
                }
                return Response(data=results, status=400)
        else:
            # 其它情况反回无内容
            return Response(status=204)
