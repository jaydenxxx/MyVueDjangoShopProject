from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd, HotSearchWords
from rest_framework import serializers


class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerilizer(serializers.ModelSerializer):
    category = CategorySerilizer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class CategorySerilizer3(serializers.ModelSerializer):
    '''
    三级目录
    '''
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerilizer2(serializers.ModelSerializer):
    '''
    二级目录
    '''
    sub_cat = CategorySerilizer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerilizer1(serializers.ModelSerializer):
    '''
    一级目录，通过model的反向查询字段sub_cat关联
    '''
    sub_cat = CategorySerilizer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"
