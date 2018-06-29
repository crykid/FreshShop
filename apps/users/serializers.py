"""
File name  : serializers.py
Created by : blank
Created on : 2018/2/6
Created at : 16:48
Created with: Intelj Pycharm
Description: 
"""
# Create your models here.
import re
from datetime import datetime
from datetime import timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from FreshShop.settings import REGEX_MOBILE, SMS_CODE_LENGTH
from .models import VerifyCode, UserProfile

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """

    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """

    """

    code = serializers.CharField(max_length=SMS_CODE_LENGTH, min_length=SMS_CODE_LENGTH, help_text="验证码",
                                 label="验证码",
                                 write_only=True,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",

                                 })
    username = serializers.CharField(required=True, allow_blank=False,
                                     label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用户已经存在")])
    password = serializers.CharField(style={"input_type": "password"}, label="密码", write_only=True)

    # def create(self, validated_data):
    #     """
    #     password 加密
    #     :param validated_data:
    #     :return:
    #     """
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        """

        :param code:
        :return:
        """
        sms_err_msg = "验证码错误"
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        # 使用filter而不用get是因为在get情况下需要考虑不存在或存在多个的情况
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_records = verify_records[0]

            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_records.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError(sms_err_msg)
        else:
            raise serializers.ValidationError(sms_err_msg)

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户信息序列化类
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email","mobile")
