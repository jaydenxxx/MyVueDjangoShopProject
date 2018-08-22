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

from .models import VerifyCode

User = get_user_model()


class SmsSerilizer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在！")

        # 验证手机号码是否合法
        # if re.match(REGEX_MOBILE, mobile):
        #     raise serializers.ValidationError("手机号码不合法！")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile