"""
File name  : signals.py
Created by : blank
Created on : 2018/2/7
Created at : 00:10
Created with: Intelj Pycharm
Description: 
"""
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
