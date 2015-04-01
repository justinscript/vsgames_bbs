#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    # # -*- coding: utf-8 -*-: it is necessary while coding with chinese
    # @csrf_exempt: add this while getting post request
    # bbs.custom_proc: get the default context for template,used for render_to_response
'''
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from bbs.custom_proc import cp_main_page
from datas.models import Topic

#the main page /index
def index(request):
    return get_main_page_response(request)

@csrf_exempt
def test(request):
    #u = UserInfo(user=t_user, description='test user info')
    #u.save()
    #u.image.save(name=request.FILES.get('file').name, content = request.FILES.get('file'))
    #
    print 'test'
    for t in Topic.objects.filter(replys=None):
        a= t.is_top
        b= not t.is_top
        print a, b
    
# use it for redirecting to main page
def get_main_page_response(request):
    #get the default context in main page by cp_main_page
    rc = RequestContext(request, processors=[cp_main_page])
    #return render_to_response('index.html')
    return render_to_response('index.html', context_instance= rc)