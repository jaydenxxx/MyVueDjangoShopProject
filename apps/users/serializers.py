#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 21:22
# @Author  : yangxi
# @File    : serializers.py
# @Software: PyCharm
import re
from datetime import datetime, timedelta
from Shop.settings import REGEX_MOBILE
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import VerifyCode

User = get_user_model()


class SmsSerilizer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, error_messages={
        "blank": "手机号不能为空！",
    })

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在！")

        # 验证手机号码是否合法
        if re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法！")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, label="验证码", max_length=4, min_length=4,
                                 error_messages={
                                     "required": "请输入验证码！",
                                     "blank": "请输入验证码！",
                                     "max_length": "验证码格式错误！",
                                     "min_length": "验证码格式错误！",

                                 },)

    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在！")])
    password = serializers.CharField(required=True, allow_blank=False, write_only=True, help_text="密码", label="密码", style={"input_type": "password"})
    
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # filters取出的为数组格式
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 验证码过期
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期！")
            # 验证码与最后一条不符合
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误！")
        else:
            raise serializers.ValidationError("验证码错误！")

    def validate(self, attrs):
        """
        全局验证序列化字段
        :param attrs:所有序列化字段的字典
        :return:
        """
        # 将username值赋值给mobile
        attrs["mobile"] = attrs["username"]
        # 因为User模型中不存在该字段，所以验证时需要删除code字段
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
