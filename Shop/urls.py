"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.views.static import serve

from Shop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CatetoryViewSet

router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name="goods")

router.register(r'categories', CatetoryViewSet, base_name="categories")

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('xadmin/', xadmin.site.urls),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),
    # router的path路径
    re_path('^', include(router.urls)),
    path('docs/', include_docs_urls(title='API接口文档')),
    # DRF自带token认证方式
    # path('api-token-auth/', views.obtain_auth_token),
    # JWT认证方式
    path('login/', obtain_jwt_token)
]
