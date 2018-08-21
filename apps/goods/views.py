from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerilizer, CategorySerilizer1
from .filters import GoodsFilter

# Create your views here.

class GoodsPagination(PageNumberPagination):
    '''
    商品列表分页类
    '''
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 15


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    商品列表
    retrieve:
    单个商品信息
    """
    pagination_class = GoodsPagination
    serializer_class = GoodsSerilizer
    queryset = Goods.objects.all()
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CatetoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        具体一级类详情分类数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerilizer1
