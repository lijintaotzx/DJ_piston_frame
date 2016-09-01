from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from piston.resource import Resource
from accounts.api.handlers import *


from django.contrib.auth.decorators import login_required

login = login_required(login_url='/wapi/accounts/user/login/')

userhandler = Resource(UserHandler)
userprohandler = Resource(UserProFileHandler)
urlpatterns = patterns('',
                       url(r'^user/register/$', userhandler),
                       url(r'^user/(?P<login>login)/$', userhandler),
                       url(r'^user/(?P<logout>logout)/$', userhandler),
                       url(r'^userpro/$', login(userprohandler)),

                       )
