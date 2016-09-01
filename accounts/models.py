
# -*- coding:UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
__author__ = 'ljt'

class TestModel(models.Model):
    name = models.CharField(max_length=10)

    def _valueDict(self):
        return {'id':self.id,'name':self.name}
    valueDict = property(_valueDict)

# class Users(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=30)
#
#     def _valueDict(self):
#         return {'id':self.id,'username':self.username}
#     valueDict = property(_valueDict)

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='userprofile')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=30)

    def _valueDict(self):
        return {'user':self.user,'phone':self.phone,'address':self.address}
    valueDict = property(_valueDict)



#用户注册后自动创建userprofile
def create_userpro(sender, instance, created, **kwargs):
    if created:
        print instance.id
        UserProfile.objects.create(user=instance, phone='',address='')
        print 'userpro create success...'

post_save.connect(create_userpro,sender=User)

