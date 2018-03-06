"""
File name  : permissions.py
Created by : blank
Created on : 2018/3/6
Created at : 18:13
Created with: Intelj Pycharm
Description: 
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
