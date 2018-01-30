from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import mixins, generics, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .filters import GoodsFilter

from .serializer import GoodsSerializer, CategorySerializer
from .models import Goods, GoodsCategory


# Create your views here.

# v2.0版本
# class GoodsListView(APIView):
#     """
#     List all goods，使用apiview，图片地址不会自动封装，也没有分页功能
#     """
#
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         # many=True表示是数组
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)

# v3.0版本
# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     """
#     List all goods，restframework完成了图片地址自动封装，没有分页
#     """
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     # 不重写get，post 等方法则默认不允许调用这些方法
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# v4.0-v6.0使用的分页
class GoodsPagination(PageNumberPagination):
    """
    设置分页功能，设置了这个就不需要在setting里面配置REST_FRAMEWORK分页配置了，
    v4.0-v6.0使用的分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


# # v4.0版本
# class GoodsListView(generics.ListAPIView):
#     """
#     使用这个，分页才会起效，有了分页功能
#     List all goods
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination

# v5.0版本
class GoodsListVeiwSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表，包含：分页，搜索，过滤，排序功能
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # 配置过滤功能
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 这样只是精确匹配
    filter_fields = ("name", "shop_price")
    filter_class = GoodsFilter
    # 字段前面加一些特殊符号表示不同的意义："^"start-with，"="exact matches，"@"full-text search,"$"regex search
    search_fields = ("name", "id")
    # 排序
    ordering_fields = ("sold_num", "add_time")


# 只要继承中间哪个RetrieveModelMixin就可以查询单个详情
class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
