# -*- coding:utf-8 -*-
from django.urls import path

from account.views.ticket import (
    TicketListApiView,
    TicketDetailApiView,
    TicketCheckApiView
)

urlpatterns = [
    # 前缀：/api/v1/account/ticket
    path("list", TicketListApiView.as_view(), name="list"),
    path("<int:name>", TicketDetailApiView.as_view(lookup_field="name"), name="detail"),
    path("check", TicketCheckApiView.as_view(), name="check"),
]
