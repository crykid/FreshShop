"""
File name  : filters.py
Created by : blank
Created on : 2018/1/28
Created at : 18:05
Created with: Intelj Pycharm
Description: 
"""

import django_filters
from .models import Goods


class GoodsFilter(django_filters.FilterSet):
    """

    """
    price_min = django_filters.NumberFilter(name="shop_price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    name = django_filters.CharFilter(name="name", lookup_expr="icontains")

    class Meta:
        model = Goods
        fields = ["price_min", "price_max", "name"]
