"""
File name  : serializer.py
Created by : blank
Created on : 2018/1/25
Created at : 23:43
Created with: Intelj Pycharm
Description: 
"""

from rest_framework import serializers
from goods.models import Goods, GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     """
#
#     """
#     name = serializers.CharField(required=True, allow_blank=True, max_length=30)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Goods` instance, given the validated data.
#         """
#         return Goods.objects.create(**validated_data)

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
      商品类别序列化
      """
    # many=True一定不要漏掉
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """
    直接通过model映射
    """
    category = CategorySerializer()

    class Meta:
        model = Goods
        # fields = ('id', 'name', 'click_num', 'market_price', 'add_time')
        fields = "__all__"
