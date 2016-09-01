# -*- coding:utf-8 -*-
from piston.handler import BaseHandler
from django.http import Http404,HttpResponse
from accounts.models import *
from piston.utils import validate, FormValidationError
import logging
from django.shortcuts import get_object_or_404
from accounts.forms import RegisterForm,LoginForm,UserProForm
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
log = logging.getLogger('root')
from django.contrib.auth.decorators import login_required


class UserHandler(BaseHandler):
    allowed_methods = ('POST','PUT')
    fields = ()

    def read(self, request, *args, **kwargs):
        return "accounts_read"


    def create(self, request, *args, **kwargs):
        if kwargs.get('login',False):
            f = LoginForm(request.POST)
            if f.is_valid():
                user = authenticate(username = f.cleaned_data['username'],password = f.cleaned_data['password'])
                if user:
                    auth_login(request,user)
                    return user
                else:
                    return HttpResponse({'error_code':1,'error_msg': u'登录失败，请使用正确的用户名和密码'}, status=400)
            raise FormValidationError(f)
        if kwargs.get('logout',False):
            auth_logout(request)
            return 'logout ok!'
        uf = RegisterForm(request.POST)
        if uf.is_valid():
            if uf.cleaned_data['password1'] != uf.cleaned_data['password2']:
                return HttpResponse({'error_code':1,'error_msg':u'两次输入的密码不一致!'},status=400)
            if len(User.objects.filter(username=uf.cleaned_data['username'])):
                return HttpResponse({'error_code':2,'error_msg':u'该用户名已经被注册!'},status=400)
            user = User.objects.create_user(username = uf.cleaned_data['username'],password=uf.cleaned_data['password1'])
            user.save()
            return user
        raise FormValidationError(uf)



    def delete(self, request, *args, **kwargs):
        return "accounts_delete"


    def update(self, request, *args, **kwargs):
        return "accounts_update"

class UserProFileHandler(BaseHandler):
    allowed_methods = ('GET','POST','PUT')
    fields = ()

    def read(self, request, *args, **kwargs):
        return "accounts_read"


    def create(self, request, *args, **kwargs):
        return "accounts_delete"


    def delete(self, request, *args, **kwargs):
        return "accounts_delete"

    def update(self, request, *args, **kwargs):
        # return 1
        userpro = request.user.userprofile
        if request.PUT.get('phone'):
            userpro.phone = request.PUT.get('phone')
        if request.PUT.get('address'):
            userpro.address = request.PUT.get('address')
        userpro.save()
        return userpro.valueDict

