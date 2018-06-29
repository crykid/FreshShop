from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from random import choice

from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import SmsSerializer, UserRegSerializer, UserProfileSerializer
from utils.yunpian import YunPian
from FreshShop.settings import APIKEY, SMS_CODE_LENGTH

from .models import VerifyCode, UserProfile

from utils.permissions import IsOwnerOrReadOnly

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


class UserViewset(CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    用户操作
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    # 添加JSONWebTokenAuthentication之后浏览器不会弹出认证窗口，弹出框是basic的一种认证模式，当前情况下需要的是浏览器中配置session
    # 添加sessionAuthen，方便浏览器使用
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        """
        重写获取serializer的方法
        :return:
        """
        # 如果是查询时需要权限，返回认证的实例数组-
        if self.action == "retrieve":
            return UserProfileSerializer
        # action==create，即注册的时候不需要权限
        elif self.action == "create":
            return UserRegSerializer
        return UserProfileSerializer

    # 检查登录权限,但是在此处配置会导致注册出问题，因为注册是不需要登录权限的
    # permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        重写获取权限的方法
        :return: 权限的实例
        """

        # 如果是查询时需要权限，返回认证的实例数组-
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        # action==create，即注册的时候不需要权限
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        """
        用户注册
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 获取token
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        和mixins的,mixins.RetrieveModelMixin配合使用,返回当前的用户
        :return:
        """
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class UserProfileViewset(viewsets.ModelViewSet):
    """
    获取用户信息
    """
    queryset = UserProfile.objects.all()
    serializers_class = UserProfileSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)
