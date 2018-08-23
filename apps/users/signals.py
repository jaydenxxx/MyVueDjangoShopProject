#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 22:39
# @Author  : yangxi
# @File    : signals.py
# @Software: PyCharm

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # instance既User实例化对象
        password = instance.password
        instance.set_password(password)
        instance.save()
