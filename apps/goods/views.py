from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerilizer, CategorySerilizer1

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
    pagination_class = GoodsPagination
    serializer_class = GoodsSerilizer
    queryset = Goods.objects.all()


class CatetoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerilizer1
