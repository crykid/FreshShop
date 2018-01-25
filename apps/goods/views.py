from django.shortcuts import render
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Goods
from .serializer import GoodsSerializer


# Create your views here.

class GoodsListView(APIView):
    """
    List all goods
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        # many=True表示是数组
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)


