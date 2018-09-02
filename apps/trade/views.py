from django.shortcuts import render
import time
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer


# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    list:
        购物车列表页
    """
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ShopCartSerializer
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    """
    list:
        获取个人订单列表
    delete:
        删除订单
    create:
        新增订单
    retrieve:
        订单商品和数量详情
    """
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        # 获取商品详情
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        # 将购物信息添加到订单关联表中
        # 删除订单信息，关联表数据也会同时删除
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            # 删除购物车中已添加到订单的数据
            shop_cart.delete()

        return order
