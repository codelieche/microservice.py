# -*- coding:utf-8 -*-
from django.urls import path, include


urlpatterns = [
    # 前缀：/api/v1
    path('store/', include(arg=('store.urls.api', 'store'), namespace='store')),
]