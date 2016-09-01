# -*- coding:UTF-8 -*-
__author__ = 'ljt'
from django import forms
from accounts.models import UserProfile


# class UserForms(forms.ModelForm):
#     class Meta:
#         model = Users
#
#     def clean_check_type(self):
#         username = self.cleaned_data['username']
#         print username
#         if username == '123':
#             raise forms.ValidationError('无效!')
#             # def __init__(self,*args,**kwargs):
#             #     self.request = kwargs.pop('request',None)
#             # username = forms.CharField(max_length=20)
#             # password = forms.CharField(max_length=30)


class RegisterForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def pwd_validate(self, p1, p2):
        return p1 == p2

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        file = ('user','address',)
