"""FreshShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from FreshShop.settings import MEDIA_ROOT
from django.views.static import serve
# from django.contrib import admin
import xadmin
from rest_framework.documentation import include_docs_urls

# v1.0
# from goods.views_base import GoodsListView

# v2.0
# from goods.views import GoodsListView
from goods.views import GoodsListVeiwSet, CategoryViewset

# v6.0,使用router，自动对v5.0做处理
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# 配置goods的url
router.register(r'goods', GoodsListVeiwSet)
# 配置categories的url
router.register(r'categories', CategoryViewset)

# v5.0
# goods_list = GoodsListVeiwSet.as_view({
#     'get': 'list',  # 把get请求绑定在list上
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 配置图片资源访问路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # v1.0-v4.0使用
    # url(r'goods/$', GoodsListView.as_view(), name="goods-list"),
    # v5.0使用
    # url(r'goods/$', goods_list, name="goods-list"),

    url(r'^', include(router.urls)),
    url(r'docs/', include_docs_urls(title="生鲜超市")),
]
