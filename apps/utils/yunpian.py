"""
File name  : yunpian.py
Created by : blank
Created on : 2018/2/6
Created at : 14:36
Created with: Intelj Pycharm
Description: 云片发送短信
"""
import requests
import json


class YunPian(object):
    """

    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【唯一520】您的验证码为{code}，如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)
        re_dect = json.loads(response.text)
        print(re_dect)
        return re_dect


if __name__ == "__main__":
    yunpian = YunPian("6e9851b9836c8a2b118f1f4d9f563bfc")
    yunpian.send_sms("2017", "15001994037")
