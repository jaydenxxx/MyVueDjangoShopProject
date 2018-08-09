from rest_framework import mixins
from rest_framework import viewsets

from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerilizer, CategorySerilizer1

# Create your views here.


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodsSerilizer
    queryset = Goods.objects.all()


class CatetoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerilizer1
