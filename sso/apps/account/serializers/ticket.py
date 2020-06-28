# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models.user import User
from account.models.ticket import Ticket
from account.serializers.user import UserDetailSerializer


class TicketModelSerializer(serializers.ModelSerializer):
    """
    Ticket Model Serializer
    """

    user = serializers.SlugRelatedField(slug_field="username", read_only=False, queryset=User.objects.all())

    class Meta:
        model = Ticket
        fields = ("id", "name", "user", "user_id", "sessionid", "return_url", "is_active", "time_added", "time_expired")


class TicketInfoSerializer(serializers.ModelSerializer):
    """
    Ticket Info Serializer
    """
    user = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "name", "sessionid", "user", "return_url", "time_added", "time_expired")
