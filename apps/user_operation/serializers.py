#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 20:44
# @Author  : yangxi
# @File    : serializers.py
# @Software: PyCharm
from .models import UserFav
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# User = get_user_model()


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已收藏！请勿重复收藏！"
            )
        ]

        fields = ("user", "goods", "id")
