#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 20:44
# @Author  : yangxi
# @File    : serializers.py
# @Software: PyCharm
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerilizer

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# User = get_user_model()


class UserFavSerializer(serializers.ModelSerializer):
    # user默认获取当前用户，不然需要选择用户
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


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerilizer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 自动获取时间
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%H-%d %H:%M")

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message', 'message_type', 'subject', 'file', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%M-%d %H:%M")
    province = serializers.CharField(required=True, label="省份", help_text="省份", error_messages={
        "required": "省份信息不能为空！",
        "blank": "省份信息不能为空！",
    })
    city = serializers.CharField(required=True, label="城市", help_text="城市", error_messages={
        "required": "城市信息不能为空！",
        "blank": "城市信息不能为空！",
    })
    district = serializers.CharField(required=True, label="区", help_text="区", error_messages={
        "required": "区信息不能为空！",
        "blank": "区信息不能为空！",
    })
    address = serializers.CharField(required=True, label="详细地址", help_text="详细地址", max_length=100, error_messages={
        "required": "地址信息不能为空！",
        "blank": "地址信息不能为空！",
        "max_length": "地址信息最长100个字符",

    })
    signer_name = serializers.CharField(required=True, label="签收人", help_text="签收人", min_length=1, max_length=20, error_messages={
        "required": "签收人信息不能为空！",
        "blank": "签收人信息不能为空！",
        "max_length": "签收人信息最长20个字符",
        "min_length": "签收人信息最少1个字符",
    })

    class Meta:
        model = UserAddress
        fields = ('user', 'province', 'city', 'district', 'address', 'signer_name', 'add_time', 'id')
