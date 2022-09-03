# -*- coding:utf-8 -*-


class BaseQuerysetFilterMixin:
    """
    根据自定义的某些字段过滤queryset
    """

    # 想根据那个字段过滤就配置那个字段过滤
    filter_filed_name = None

    def get_filter_field_value(self):
        # 获取过滤字段的值
        # return self.request.user.team_id
        return None

    def get_filter_params(self):
        # 如果想实现多个字段过滤，直接复写这个方法即可

        # 1. 判断是否配置了过滤的字段
        if self.filter_filed_name:
            # 2. 获取过滤的值
            value = self.get_filter_field_value()
            if value is not None:
                params = {
                    self.filter_filed_name: value
                }
                return params
            else:
                return None
        else:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filter_filed_name and queryset:
            params = self.get_filter_params()
            # 如果过滤params得到的是个dict，那么就执行过滤
            if params and isinstance(params, dict):
                queryset = queryset.filter(**params)
        return queryset


class QuerysetFilterByTeamID(BaseQuerysetFilterMixin):
    """
    根据teamid过滤queryset
    """

    # 每个需要根据team_id过滤的视图，请自行设置team_id_field
    # team_id_field = None

    def get_filter_field_value(self):
        try:
            return self.request.user.team_id
        except Exception as e:
            return None

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.team_id_field and queryset:
    #         params = {
    #             self.team_id_field: self.get_team_id_value()
    #         }
    #         queryset = queryset.filter(**params)
    #     return queryset
