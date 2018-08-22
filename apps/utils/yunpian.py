#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 20:51
# @Author  : yangxi
# @File    : yunpian.py
# @Software: PyCharm
import requests
import json


class YunPian():
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【杨曦TECH】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code),
        }
        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict