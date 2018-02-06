from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from random import choice

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import SmsSerializer, UserRegSerializer
from utils.yunpian import YunPian
from FreshShop.settings import APIKEY, SMS_CODE_LENGTH

from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
#     """
#     发送短信验证码
#     """
#     serializer_class = SmsSerializer
#
#     def generate_code(self):
#         """
#         生成四位数字的验证码
#         :return:
#         """
#         seeds = "1234567890"
#         random_str = []
#         for i in range(4):
#             random_str.append(choice(seeds))
#
#         return "".join(random_str)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         mobile = serializer.validated_data["mobile"]
#
#         yun_pian = YunPian(APIKEY)
#
#         code = self.generate_code()
#
#         sms_status = yun_pian.send_sms(code=code, mobile=mobile)
#
#         if sms_status["code"] != 0:
#             return Response({
#                 "mobile":sms_status["msg"]
#             }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             code_record = VerifyCode(code=code, mobile=mobile)
#             code_record.save()
#             return Response({
#                 "mobile":mobile
#             }, status=status.HTTP_201_CREATED)


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    # YUNPIAN_SMS_SEND_SUCCESS = 0

    def generate_code(self):
        """
        生成4位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(SMS_CODE_LENGTH):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        # 获取到我们定义的serializer_class
        serializer = self.get_serializer(data=request.data)
        # 当true的时候这一步出问题就直接抛异常，不会再执行以后的代码
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response(
                #     {
                #     "code": sms_status["code"],
                #     "mobile": mobile,
                #     "msg": sms_status["msg"]
                # }
                sms_status, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 发送成功后保存验证码
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()

            return Response(sms_status, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
