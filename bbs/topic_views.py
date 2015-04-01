#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User
from datas.models import Topic, Node, UserInfo
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from bbs.custom_proc import cp_main_page
from bbs import myforms
from django.http.response import HttpResponseRedirect, JsonResponse
from returncode import jsoncode as jsC
from myutils import CoinsController as c_control
from bbs.returncode import add_item
# views for any action about topic
@csrf_exempt
@login_required(login_url='/login')  
def post_topic(request):
    if request.method != 'POST':
        node_list = Node.objects.exclude(on_home=True)
        return render_to_response('release_topic.html', {'node_list': node_list},RequestContext(request))
    
    t_form = myforms.topic_form(request.POST)
    if t_form.is_valid():
        f_node = Node.objects.get(id=t_form.cleaned_data['classify'])
        f_title = t_form.cleaned_data['title']
        f_content = t_form.cleaned_data['content']
        topic = Topic(node=f_node, title=f_title, content=f_content, user=request.user)
        topic.save()
        c_control.commit(request.user, c_control.POST_TOPIC)
        return JsonResponse(jsC.success)
    else:
        return JsonResponse(jsC.fail)

@csrf_exempt
@login_required(login_url='/login')  
def reply_topic(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/index/')
    t_form = myforms.reply_form(request.POST)
    if t_form.is_valid():
        topic_id = t_form.cleaned_data['topic_id']  
        if Topic.objects.filter(id=topic_id).exists():
            topic = Topic.objects.get(id=topic_id)
            f_node = topic.node
            f_content = t_form.cleaned_data['content']
            reply = Topic(node=f_node, content=f_content, user=request.user, replys=topic)
            reply.save()
            if not (Topic.objects.filter(replys=topic, user=request.user).exclude(id=reply.id).exists()\
            or request.user.id == topic.user.id ):
                c_control.commit(request.user, c_control.REPLY_TOPIC)
            # successful
            return JsonResponse(jsC.success)
        else:
            # topic is not existed
            return JsonResponse(jsC.fail)
    else:
        return JsonResponse(jsC.fail)
 
# display the topic content
def display_topic(request,topic_id):
    if not topic_id:
        return HttpResponseRedirect('/index/')
    # get a topic depending on topic_id from url
    if Topic.objects.filter(id=topic_id, is_active=True, replys=None).exists():
        topic = Topic.objects.get(id=topic_id)
        topic.set_is_read(request.user)
        # increase hits
        topic.hits +=1
        topic.save()
        votes = topic.vote_user.count()
        user = request.user
        is_voted = True if (user.is_authenticated() and not user.userinfo.vote.filter(id=topic_id).exists()) else False
        # get replys in the topic
        replys = Topic.objects.filter(replys=topic, is_active=True).order_by('created')
        return render_to_response('display_topic.html',
                                  {'topic': topic, 
                                   'replys': replys,
                                   'votes': votes,
                                   'is_voted': is_voted},
                                  RequestContext(request, processors=[cp_main_page]))
    else:
        return HttpResponseRedirect('/index/')

@csrf_exempt
@login_required(redirect_field_name=None, login_url='/login')
def vote_topic(request):
    if request.method != 'POST':
        return JsonResponse(jsC.fail)
    topic_id = request.POST['topic_id']
    if Topic.objects.filter(id=topic_id, is_active=True).exists():
        topic = Topic.objects.get(id=topic_id)
        if topic.user.id == request.user.id:
            return JsonResponse(add_item(jsC.fail, 'msg', '不能给自己点赞'))
        request.user.userinfo.vote.add(topic)
        c_control.commit(topic.user, c_control.VOTED)
        return JsonResponse(jsC.success)
    else:
        return JsonResponse(jsC.fail)

@csrf_exempt
@login_required(redirect_field_name=None, login_url='/login')    
def delete_topic(request):
    if request.method != 'POST':
        return JsonResponse(jsC.fail)
    topic_id = request.POST.get('topic_id')
    if Topic.objects.filter(id=topic_id, is_active=True).exists():
        topic = Topic.objects.get(id=topic_id)
        if topic.node.mayor.filter(id=request.user.id).exists():
            topic.is_active = False
            topic.save()
            return JsonResponse(jsC.success)
        return JsonResponse(jsC.fail)
    else:
        return JsonResponse(jsC.fail)

@csrf_exempt
@login_required(redirect_field_name=None, login_url='/login')    
def set_topic_top(request):
    if request.method != 'POST':
        return JsonResponse(jsC.fail)
    topic_id = request.POST.get('topic_id')
    if Topic.objects.filter(id=topic_id, is_active=True).exists():
        topic = Topic.objects.get(id=topic_id)
        if topic.node.mayor.filter(id=request.user.id).exists():
            topic.is_top = not topic.is_top
            topic.save()
            return JsonResponse(jsC.success)
        return JsonResponse(jsC.fail)
    else:
        return JsonResponse(jsC.fail)
   
@csrf_exempt
@login_required(redirect_field_name=None, login_url='/login')
def fav_topic(request):
    if request.method != 'POST':
        return JsonResponse(jsC.fail)
    topic_id = request.POST.get('topic_id')
    if Topic.objects.filter(id=topic_id, is_active=True).exists():
        topic = Topic.objects.get(id=topic_id)
        request.user.userinfo.fav.add(topic)
        request.user.userinfo.save()
        return JsonResponse(jsC.success)
    else:
        return JsonResponse(jsC.fail)