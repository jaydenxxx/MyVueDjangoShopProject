#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/2 15:04
# @Author  : yangxi
# @File    : serializers.py
# @Software: PyCharm
import time
from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerilizer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerilizer(many=False)

    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label="数量", help_text="数量",
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "required": "请选择商品数量",
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(goods=goods, user=user)

        # 商品已存在，更新数量
        if existed:
            existed = existed[0]
            existed.nums = nums
            existed.save()
        # 商品不存在新增
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        import random
        random_ins = random.Random()
        # 订单号生成规则为时间（精确到秒）+用户id+两位随机数
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # 提前为订单生成订单号
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    # 该goods序列化才是真正的商品详情序列化
    goods = GoodsSerilizer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    # 该序列化goods为订单关联表中的goods
    # 有可能一个订单会包含多个goods
    # 每个商品还包含数量，所以商品详情的序列化应该是Order中的goods
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"
