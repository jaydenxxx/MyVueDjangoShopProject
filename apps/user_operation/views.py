from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly

from .models import UserFav
from .serializers import UserFavSerializer
# Create your views here.


class UserFavViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 权限系统，用于验证用户是否登录和操作是否为创建者
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    lookup_field = "goods_id"
    # 只获取当前用户的收藏
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)