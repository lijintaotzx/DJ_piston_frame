
#-*- coding:utf-8 -*-
from piston.handler import BaseHandler
from django.http import Http404
from models import *
from piston.utils import validate
import logging
from django.shortcuts import get_object_or_404

log = logging.getLogger('root')

class MyHandler(BaseHandler):
    allowed_methods = ('POST', 'GET', 'DELETE', 'PUT')
    #model = {}
    fields = ()

    def read(self, request, *args, **kwargs):
        return "accounts_read"

    def create(self, request, *args, **kwargs):
        return "accounts_create"

    def delete(self, request, *args, **kwargs):
        return "accounts_delete"

    def update(self, request, *args, **kwargs):
        return "accounts_update"