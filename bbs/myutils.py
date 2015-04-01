#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import types

# input a datetime,return string for display depending on (now-time_in)
def get_delta_time(time_in):
    time_delta = datetime.today() - time_in
    day = time_delta.days
    sec = time_delta.seconds
    if  day > 0:
        if day/365 > 0:
            return '%d 年前' % (day/365)
        else:
            return '%d 天前' % (day%365)
    else:
        if sec < 60:
            return '1 分钟前'
        elif sec < 3600:
            return '%d 分钟前' % (sec/60)
        else:
            return '%d 小时 %d 分钟前' % (sec/3600, (sec%3600)/60)
        
# get token for sending email depending on user
def get_token(user):
    m = hashlib.md5()
    m.update(user.username)
    m.update(user.password)
    m.update(user.email)
    return m.hexdigest()


# send an email
def my_send_email(url, email):
    msg = '点击链接继续重置密码: '.decode('utf-8')
    send_mail(subject='黑狮情报所-激战2玩家社区 密码重置验证', message= msg+ url, 
    from_email='ljq430001098@126.com', recipient_list=[email] ,
    fail_silently=False)
   
PAGE_SIZE = 5
# paging the queryset depending on 'page' attribute
def paging(request, query_set):
    paginator = Paginator(query_set, PAGE_SIZE) # Show PAGE_SIZE contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return contacts

class CoinsController:
    # replying topic: get 1
    REPLY_TOPIC = 0
    POST_TOPIC = 1
    VOTED = 2
    UNUSED = 3
    CUT = 4
    
    delta = (5, 10, 1, -15, -50)
    @staticmethod
    def commit(user, ctype, coins=None):
        coins = CoinsController.delta[ctype] if type(coins) != types.IntType else coins
        try:
            user.userinfo.coins += coins
            user.userinfo.save()
            return True
        except:
            return False