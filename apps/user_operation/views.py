from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFravViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    """
    用户收藏功能
    """
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 登录认证--用于权限限制，仅仅可以对自己的数据进行操作
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # 使用token认证
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
