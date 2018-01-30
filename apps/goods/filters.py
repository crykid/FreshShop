"""
File name  : filters.py
Created by : blank
Created on : 2018/1/28
Created at : 18:05
Created with: Intelj Pycharm
Description: 
"""

import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # gte大于等于
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr='gte')
    # lte小于等于
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    # contains 包含，用于模糊查询
    # name = django_filters.CharFilter(name="name", lookup_expr="icontains")
    top_category = django_filters.NumberFilter(method="top_category_filter")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(
            Q(category_id=value) | Q(category__parent_category_id=value) | Q(
                category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ["pricemin", "pricemax"]
