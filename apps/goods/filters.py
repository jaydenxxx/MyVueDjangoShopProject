#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 22:16
# @Author  : yangxi
# @File    : filters.py
# @Software: PyCharm

from django.db.models import Q
import django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    top_category = django_filters.NumberFilter(field_name='top_category', method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name']