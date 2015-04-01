#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    # # -*- coding: utf-8 -*-: it is necessary while coding with chinese
    # @csrf_exempt: add this while getting post request
    # bbs.custom_proc: get the default context for template,used for render_to_response
'''
from django.http import HttpResponse
from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User
from datas.models import Topic, Node, UserInfo, Letter
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from bbs import myforms
from django.http.response import HttpResponseRedirect
from returncode import jsoncode as jsC
from returncode import add_item
from myutils import get_token, my_send_email

#singup function,require username and password,only response POST
@csrf_exempt
def signup(request):
    # has logined,redirect to main page
    if(request.user.is_authenticated()):
        return HttpResponseRedirect('/index/')
    # if it is not POST,redirect to sigup page
    if request.method != 'POST':
        return render_to_response('signup.html')
    # it is POST
    s_form = myforms.signup_form(request.POST)
    if s_form.is_valid(): 
        f_username = s_form.cleaned_data['username']
        f_password = s_form.cleaned_data['password']
        #f_repassword = s_form.cleaned_data['repassword']
        #TODO should check email
        f_email = s_form.cleaned_data['email']
        if not User.objects.filter(username=f_username).exists() :
            user = User.objects.create_user(
                        username = f_username, 
                        password = f_password,
                        email=f_email)
            UserInfo(user=user).save()
            # login after singup sucessfully
            s_user = authenticate(username=f_username, password=f_password)
            login(request, s_user)
            return JsonResponse(jsC.success)
        # is username exists
        return JsonResponse(jsC.fail)
    else:
        # form data is incorrect
        return JsonResponse(jsC.fail)

@csrf_exempt
def vlogin(request):
    # get next page if url has, if not set it 'index'
    next_page = get_redirect(getdic=request.GET, default= '/index/')
    # if has logined,redirect to next page,default is main page
    if(request.user.is_authenticated()):
        return HttpResponseRedirect(next_page)
    # return login.html directly,if it is GET method
    if request.method != 'POST':
        return render_to_response('login.html')
    # POST method
    else:
        # get post data
        l_form = myforms.login_form(request.POST)
        if l_form.is_valid():
            f_username = l_form.cleaned_data['username']
            f_password = l_form.cleaned_data['password']
            # log user in
            user = authenticate(username=f_username, password=f_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # login successfully
                    return JsonResponse(jsC.success)
                else:
                    # user is not active
                    return JsonResponse(jsC.fail)
            else:
                # user is not existed
                return JsonResponse(jsC.fail)
        else:
            # form data is incorrect
            return JsonResponse(jsC.fail)

# if user is not logined, direct to index
@login_required(redirect_field_name=None, login_url='/index')
def vlogout(request):
    logout(request)
    # redirect to a success page
    return HttpResponseRedirect('/index/')

@csrf_exempt
# forget password, send an email to user
def vforget(request):
    # not POST method
    if request.method != 'POST':
        return render_to_response('forget_pwd.html')
    # POST method
    else:
        if request.POST.get('email'):
            email = request.POST.get('email')
            # email exists
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                token = get_token(user)
                attr = '/resetpwd2/?token=%s&u=%s' % (token, user.username)
                url = 'http://'+ request.get_host() + attr
                my_send_email(url, email)
                # send an email
                return JsonResponse(add_item(jsC.success, 'msg', '发送成功'))
            else:
                return JsonResponse(add_item(jsC.fail, 'msg', '邮箱未注册'))
        else:    
            return JsonResponse(add_item(jsC.fail, 'msg', '请输入邮箱'))

@csrf_exempt
@login_required(redirect_field_name=None, login_url='/index/')
def resetpwd_bypwd(request):
    if request.method != 'POST':
        return render_to_response('reset_pwd.html',RequestContext(request))
    cp_form = myforms.resetpwd_form(request.POST)
    if cp_form.is_valid():
        old_password = cp_form.cleaned_data['old_password']
        password = cp_form.cleaned_data['new_password']
        if request.user.check_password(old_password):
            request.user.set_password(password)
            request.user.save()
            return JsonResponse(add_item(jsC.success, 'msg', '修改成功'))
    return JsonResponse(add_item(jsC.fail, 'msg', '修改失败'))


@csrf_exempt
def resetpwd_byemail(request):
    if request.user.is_authenticated():
        logout(request)
    # if contains 'email' and 'token', it is an url from email
    if request.method == 'GET' and request.GET.get('u') and request.GET.get('token'):
        username = request.GET.get('u')
        # if email exists
        if User.objects.filter(username=username).exists():
            token1 = request.GET.get('token')
            user = User.objects.get(username=username)
            token2 = get_token(user)
            # if two tokens are the same, direct to reset password
            if token1 == token2:
                return render_to_response('reset_pwd2.html')
            else:
                raise Http404()
        # email not exists
        else:
            raise Http404()
    elif request.method == 'POST':
        p_form = myforms.login_form(request.POST)
        if p_form.is_valid():
            username = p_form.cleaned_data['username']
            if User.objects.filter(username = username).exists():
                password = p_form.cleaned_data['password']
                user = User.objects.get(username = username)
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return JsonResponse(add_item(jsC.success, 'msg', '重置密码成功'))
        return JsonResponse(add_item(jsC.fail, 'msg', '参数错误'))    
    else:
        raise Http404()

@login_required(login_url='/login')
def get_my_topics(request):
    topics = request.user.topics.filter(is_active=True, replys=None)
    replys = request.user.topics.filter(is_active=True).exclude(replys=None)
    return render_to_response('mytopics.html',{'topics': topics, 'replys':replys},RequestContext(request))


@csrf_exempt
@login_required(login_url='/login')
def custom_userinfo(request):
    if request.method == 'GET':
        return render_to_response('setting_userinfo.html', RequestContext(request))
    elif request.method == 'POST':
        u_form = myforms.userinfo_form(request.POST)
        if u_form.is_valid():
            screen_name = u_form.cleaned_data['screen_name']
            description= u_form.cleaned_data['description']
            print screen_name, description
            User.objects.filter(id=request.user.id).update(first_name= screen_name)
            UserInfo.objects.filter(user=request.user).update(description= description)
            return JsonResponse(add_item(jsC.success, 'msg', '修改成功'))
        return JsonResponse(jsC.fail)
    else:
        raise Http404()

@csrf_exempt
@login_required(login_url='/login')
def custom_avatar(request):
    if request.method == 'GET':
        return render_to_response('setting_avatar.html', RequestContext(request))
    if request.method == 'POST' and request.FILES.get('file'):
        # TODO improve image uploaded function
        name=request.user.username
        content = request.FILES.get('file')
        request.user.userinfo.image.save(name=name, content=content)
        return JsonResponse(add_item(jsC.success, 'msg', '成功上传头像'))
    return JsonResponse(jsC.fail)

@login_required(login_url='/login')
def setting_page(request):
    if request.method == 'GET':
        return render_to_response('setting_index.html', RequestContext(request)) 

@csrf_exempt
def frozen_user(request):
    if not request.user.has_perm('auth.change_user'):
        return JsonResponse(add_item(jsC.fail, 'msg', '无权限'))
    if request.method =='POST' and request.POST.get('userid'):
        if User.objects.filter(id=request.POST.get('userid')).exists():
            user = User.objects.get(id=request.POST.get('userid'))
            user.is_active = not user.is_active
            user.save()
            return JsonResponse(add_item(jsC.success, 'msg', '操作成功'))
        return JsonResponse(jsC.fail)
    return JsonResponse(jsC.fail)

@csrf_exempt
def set_node_mayor(request):
    if not request.user.has_perm('datas.change_node'):
        return JsonResponse(add_item(jsC.fail, 'msg', '无权限'))
    if request.method =='POST' and request.POST.get('userid') and request.POST.get('nodeid'):
        if User.objects.filter(id=request.POST.get('userid')).exists()\
        and Node.objects.filter(id=request.POST.get('nodeid').exists()):
            user = User.objects.get(id=request.POST.get('userid'))
            node = Node.objects.get(id=request.POST.get('nodeid'))
            node.mayors.add(user)
            node.save()                        
            return JsonResponse(add_item(jsC.success, 'msg', '操作成功'))
        return JsonResponse(jsC.fail)
    return JsonResponse(jsC.fail)


@csrf_exempt
@login_required(login_url='/login')
def send_letter(request):
    if request.method =='POST':
        l_form = myforms.letter_form(request.POST)
        if l_form.isvalid():
            from_username = l_form.cleaned_data['from_username']
            to_username = l_form.cleaned_data['to_username']
            content = l_form.cleaned_data['content']
            if User.objects.filter(username=from_username).exists() and User.objects.filter(username=to_username).exists():
                from_user = User.objects.filter(username=from_username).first()
                from_user = User.objects.filter(username=to_username).first()
                letter = Letter(from_user=from_user, to_username=to_username, content=content)
                letter.save()
                return JsonResponse(add_item(jsC.success, 'msg', '发送成功'))
            return JsonResponse(add_item(jsC.fail, 'msg', '用户不存在'))
        return JsonResponse(add_item(jsC.fail, 'msg', '数据错误'))
    return JsonResponse(jsC.fail)


@csrf_exempt
@login_required(login_url='/login')
def user_topics(request, topic_type):
    temp = 'test.html'
    if topic_type == 'all':
        post_topics = request.user.topics.filter(replys=None)
        reply_topics = request.user.topics.exclude(replys=None)
        fav_topics = request.user.userinfo.fav.filter(is_active=True)
        vote_topics = request.user.userinfo.vote.filter(is_active=True)
        return render_to_response(temp, {'post_topics': post_topics,
                                       'reply_topics': reply_topics,
                                       'fav_topics': fav_topics,
                                       'vote_topic': vote_topics}, RequestContext(request))
    elif topic_type == 'post':
        post_topics = request.user.topics.filter(replys=None)
        return render_to_response(temp, {'post_topics': post_topics}, RequestContext(request))
    elif topic_type == 'reply':
        reply_topics = request.user.topics.exclude(replys=None)
        return render_to_response(temp, {'reply_topics': reply_topics}, RequestContext(request))
    elif topic_type == 'fav':
        fav_topics = request.user.userinfo.fav.filter(is_active=True)
        return render_to_response(temp, {'fav_topics': fav_topics}, RequestContext(request))
    elif topic_type == 'vote':
        vote_topics = request.user.userinfo.vote.filter(is_active=True)
        return render_to_response(temp, {'vote_topic': vote_topics}, RequestContext(request))
    else:
        return HttpResponseRedirect('/index', RequestContext(request))

def get_redirect(getdic, default, next_name='next'):
    return getdic.get(next_name) if getdic.get(next_name) else default  
