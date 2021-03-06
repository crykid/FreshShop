"""
File name  : views_base.py
Created by : blank
Created on : 2018/1/22
Created at : 22:25
Created with: Intelj Pycharm
Description: 商品相关api
"""
from goods.models import Goods
from django.views.generic.base import View


# class GoodsListView(View):
#     def get(self, request):
#         """
#         通过django的view实现商品列表页
#         :param request:
#         :return:
#         """
#
#         json_list = []
#         goods = Goods.objects.all()[:10]
#         for good in goods:
#             json_dict = {}
#             json_dict["name"] = good.name
#             json_dict["category"] = good.category.name
#             json_dict["market_price"] = good.market_price
#             json_list.append(json_dict)
#
#         from django.http import HttpResponse
#         import json
#         return HttpResponse(json.dumps(json_list), content_type="application/json")

class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """

        json_list = []
        goods = Goods.objects.all()[:10]

        # 把取到的所有goods转化为列表的方法1：
        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category.name
        #     json_dict["market_price"] = good.market_price
        #     json_list.append(json_dict)
        #

        # 把取到的所有的goods转化为列表的方法2：
        # from django.forms.models import model_to_dict
        #
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        # 把取到的所有的goods转化为列表的方法3：
        from django.core import serializers
        import json
        json_data = serializers.serialize("json", goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse
        import json

        # return HttpResponse(json.dumps(json_list), content_type="application/json")
        # JsonResponse 是httpResponse的升级版，替它做了json转化
        return JsonResponse(json_data, safe=False)
