
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from piston.resource import Resource
from accounts.views import *

urlpatterns = patterns('',
                    url(r'^$', (TemplateView.as_view(template_name='accounts.html')),
                           name='accounts'),
    )