from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
# Create your views here.


class UserFavViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否收藏
    create:
        收藏商品
    destrory:
        取消收藏
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 权限系统，用于验证用户是否登录和操作是否为创建者
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    lookup_field = "goods_id"
    # 只获取当前用户的收藏
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        else:
            return UserFavDetailSerializer


class LeavingMessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    list:
        获取留言
    create:
        添加留言
    destory:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    list:
        获取用户所有地址
    create:
        新增用户收货地址
    destory:
        删除用户收货地址
    update:
        更新用户收货地址
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)