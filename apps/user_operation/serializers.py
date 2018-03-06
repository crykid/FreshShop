"""
File name  : serializers.py
Created by : blank
Created on : 2018/3/6
Created at : 17:07
Created with: Intelj Pycharm
Description: 
"""

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    """

    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav

        # 在model里面配置过其实这里不必配置
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="商品已被收藏")
        ]
        fields = ("user", "goods", "id")
