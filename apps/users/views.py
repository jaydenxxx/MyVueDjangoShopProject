from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from random import choice

from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerilizer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from Shop.settings import APIKEY
from .models import VerifyCode


User = get_user_model()

# Create your views here.

class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerilizer

    def generate_code(self):
        """
        生成四位数验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        #把random_str由list转换成str
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 序列化后的手机号
        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(self.generate_code(), mobile)
        # 失败
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        # 成功
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            self.perform_create(code_record)
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 若此处设置权限会导致注册也需要登录验证
    # permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_serializer_class(self):
        """
        根据不同请求获取不同序列化类
        :return:
        """
        # 获取详情时使用用户详情类
        if self.action == "retrieve":
            return UserDetailSerializer
        # 当注册时，使用注册类
        elif self.action == "create":
            return UserRegSerializer
        else:
            return UserDetailSerializer

    def get_permissions(self):
        """
        根据不同请求设置不同权限
        :return:
        """
        # 当获取详情是需要权限
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        # 当注册时，不需要权限
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        pass

    def get_object(self):
        return self.request.user
