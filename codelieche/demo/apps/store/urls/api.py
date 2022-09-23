# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views.book import BookApiViewSet
from store.views.email import EmailApiViewSet


router = DefaultRouter()


router.register("book", BookApiViewSet)
router.register("email", EmailApiViewSet)

urlpatterns = [
    # 前缀：/api/v1/store
    # 前缀: /api/v1/
    # ViewSet
    path('', include(router.urls), name="store"),
]
