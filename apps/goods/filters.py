#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 22:16
# @Author  : yangxi
# @File    : filters.py
# @Software: PyCharm

import django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    min_price = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price', 'name',]