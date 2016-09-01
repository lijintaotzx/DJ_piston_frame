#-*- coding:utf-8 -*-
import os
import sys
import shutil

__author__ = 'ljt'
'''
用于快速创建一个 web app
在命令行 进入到 本文件（web-app-admin.py）所在的目录
然后执行 python web-app-admin.py [AppName] ;app name 为参数

本脚本 会更改的文件：
 settings.py  自动将 要创建的 app 添加到 INSTALLED_APPS内
 msgcopy_web_app/urls.py 将app 的 url 添加到 urlpatterns

脚本生成的文件：
    [AppName]---|--api--__init_.py
                |   |--handlers.py
                |   └--urls.py
                |--static--[AppName]--css--[AppName].css
                |               |-------js--[AppName].js
                |               └-------images
                |---templates--[AppName].html
                |---__init__.py
                |---forms.py
                |---models.py
                |---test.py
                |---urls.py
                └---views.py

生成app后。如果您的项目在运行中。那么恭喜您，您可以直接在浏览器看到效果啦。
访问 localhost:8000/[AppName]/ 会访问到 AppName.html
访问 localhost:8000/wapi/[AppName]/ 会得到接口返回的数据 '[AppName]_read'.如果以post delete update 方式访问。得到不同的结果
接下来 您只需要更改 脚本生成的文件即可完成某个APP 的功能。
=====================================================================================
|最后一点：请注意！ 轻勿删除msgcopy_web_app/urls.py 里的#URL_END 否 本脚本无法完成url的配置|
|如有疑问，可以联系我:ljt@msgcopy.net                                                |
=====================================================================================
'''


class Files():
    api_handlers = """
#-*- coding:utf-8 -*-
from piston.handler import BaseHandler
from django.http import Http404
from WEB_APP_NAME.models import *
from piston.utils import validate
import logging
from django.shortcuts import get_object_or_404

log = logging.getLogger('root')

class MyHandler(BaseHandler):
    allowed_methods = ('POST', 'GET', 'DELETE', 'PUT')
    fields = ()

    def read(self, request, *args, **kwargs):
        return "WEB_APP_NAME_read"

    def create(self, request, *args, **kwargs):
        return "WEB_APP_NAME_create"

    def delete(self, request, *args, **kwargs):
        return "WEB_APP_NAME_delete"

    def update(self, request, *args, **kwargs):
        return "WEB_APP_NAME_update"
    """

    api_urls = """
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from piston.resource import Resource
from WEB_APP_NAME.api.handlers import *
handler = Resource(MyHandler)
urlpatterns = patterns('',
                    url(r'^$',handler),
    )
    """

    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tzx</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <link href="{{ STATIC_URL }}WEB_APP_NAME/css/WEB_APP_NAME.css?v1.0{{ VERSION }}" rel="stylesheet">
     <script type="text/javascript">
       var static_url= {{ STATIC_URL }};
    </script>
</head>
<body unselectable="on" style="-moz-user-select:none;-webkit-user-select:none;" onselectstart="return false;">
<div id="msg_layer">
    <!--这里是弹出层-->
</div>
<div id="main">
    <!-- 这里写主要内容-->
    <span style='font-size:64px;'>Hello WEB_APP_NAME</span>
</div>
<script src="{{ STATIC_URL }}js/jquery.js?v1.0{{ VERSION }}"></script>
<script src="{{ STATIC_URL }}js/kaoke/kaoke_sdk.js?v=1.0{{ VERSION }}"></script>
<script src="{{ STATIC_URL }}js/kaoke/msgcopy_script.js?v=1.0{{ VERSION }}"></script>
{{ EMULATOR }}
<script type="text/javascript" src="{{ STATIC_URL }}WEB_APP_NAME/js/WEB_APP_NAME.js?v=1.0"></script>
</body>
</html>
    '''
    js = '''
$(function(){
 //当js 加载的时候执行
});
function myfunction(){
 //在这里做你任何想做的事情
}
    '''
    css = '''
*{
 padding:0px;
 margin:0px;
}
    '''

    models = '''
# -*- coding:UTF-8 -*-
from django.db import models

__author__ = 'ljt'

    '''
    forms = '''
# -*- coding:UTF-8 -*-
__author__ = 'ljt'
from django import forms
    '''
    tests = '''
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    '''

    views = '''
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
        return "WEB_APP_NAME_read"

    def create(self, request, *args, **kwargs):
        return "WEB_APP_NAME_create"

    def delete(self, request, *args, **kwargs):
        return "WEB_APP_NAME_delete"

    def update(self, request, *args, **kwargs):
        return "WEB_APP_NAME_update"'''
    url = '''
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from piston.resource import Resource
from WEB_APP_NAME.views import *

urlpatterns = patterns('',
                    url(r'^$', (TemplateView.as_view(template_name='WEB_APP_NAME.html')),
                           name='WEB_APP_NAME'),
    )'''


if len(sys.argv) <= 1:
    exit(11)


def writeFile(path, content):
    file = open(path, 'w')
    file.write(content)
    file.close()


web_app_name = sys.argv[1]
current_dir = os.path.curdir
# 在settings 里 加入 该app
file_object = open('settings.py', 'r')
all_the_txt = file_object.read()
file_object.close()
all_the_txt = all_the_txt.replace('INSTALLED_APPS = (', 'INSTALLED_APPS = (\n    \'%s\',' % (web_app_name))
file_new = open('settings.py', 'w')
file_new.write(all_the_txt)
file_new.close()

file_object = open('urls.py', 'r')
all_the_txt = file_object.read()
file_object.close()
all_the_txt = all_the_txt.replace('#URL_END',
                                  "url(r'^wapi/%s/', include('%s.api.urls')),\n                       url(r'^%s/', include('%s.urls')),\n                       #URL_END" % (
                                  web_app_name, web_app_name, web_app_name, web_app_name))
file_new = open('urls.py', 'w')
file_new.write(all_the_txt)
file_new.close()

os.chdir('..')
print(current_dir)

try:
    shutil.rmtree(web_app_name)
except:
    pass
os.mkdir(web_app_name)
os.chdir(web_app_name)
os.mkdir('api')
writeFile('api/__init__.py', '')
writeFile('api/handlers.py', Files.api_handlers.replace('WEB_APP_NAME', web_app_name))
writeFile('api/urls.py', Files.api_urls.replace('WEB_APP_NAME', web_app_name))

os.makedirs('static/%s/css' % web_app_name)
os.makedirs('static/%s/js' % web_app_name)
os.makedirs('static/%s/images' % web_app_name)
os.makedirs('templates')
writeFile('__init__.py', '')
writeFile('views.py', Files.views.replace('WEB_APP_NAME', web_app_name))
writeFile('models.py', Files.models)
writeFile('forms.py', Files.forms)
writeFile('tests.py', Files.tests)
writeFile('urls.py', Files.url.replace('WEB_APP_NAME', web_app_name))
writeFile('templates/%s.html' % (web_app_name), Files.html.replace('WEB_APP_NAME', web_app_name))
writeFile('static/%s/js/%s.js' % (web_app_name, web_app_name), Files.js)
writeFile('static/%s/css/%s.css' % (web_app_name, web_app_name), Files.css)

print(u'%s创建成功' % web_app_name)
print(u'%s创建成功' % web_app_name)
print(u'%s创建成功' % web_app_name)
print(u'%s创建成功' % web_app_name)
print(u'%s创建成功' % web_app_name)

res = u'''
        [AppName]---|--api--__init_.py
                |   |--handlers.py
                |   └--urls.py
                |--static--[AppName]--css--[AppName].css
                |               |-------js--[AppName].js
                |               └-------images
                |---templates--[AppName].html
                |---__init__.py
                |---forms.py
                |---models.py
                |---test.py
                |---urls.py
                └---views.py
'''
res = res.replace('[AppName]', web_app_name)
print '文件清单:'
print res

res =u'''
        访问 localhost:8000/[AppName]/ 会访问到 AppName.html
        访问 localhost:8000/wapi/[AppName]/ 会得到接口返回的数据 '[AppName]_read'.如果以post delete update 方式访问。得到不同的结果
'''
res = res.replace('[AppName]', web_app_name)
print res