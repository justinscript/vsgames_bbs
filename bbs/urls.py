#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from bbs import views, topic_views, account_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # admin page,unnecessary to edit
    #url(r'^admin/', include(admin.site.urls)),
    # url for test, it should be deleted finally
    #url(r'^test/$', views.test),
    # direct to home page without anything behind the path
    
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),

    url(r'^/?$', views.index),
    # home page
    url(r'^index/$', views.index),
    # singup an account
    url(r'^signup/$', account_views.signup),
    # login
    url(r'^login/$', account_views.vlogin),
    # logout
    url(r'^logout/$', account_views.vlogout),
    # forget password
    url(r'^forget/$', account_views.vforget),
    url(r'^frozenuser/$', account_views.frozen_user),
    url(r'^user/([a-z]*)/$', account_views.user_topics),
    # reset password if user know his password
    url(r'^resetpwd/$', account_views.resetpwd_bypwd),
    # reset password if user know his password
    url(r'^resetpwd2/$', account_views.resetpwd_byemail),
    url(r'^setting_index/$', account_views.setting_page),
    url(r'^setting_userinfo/$', account_views.custom_userinfo),
    url(r'^setting_avatar/$', account_views.custom_avatar),
    url(r'^mytopics/$', account_views.get_my_topics),
    url(r'^sendletter/$', account_views.send_letter),
    # display topic content,get a topic id from url
    url(r'^topic/(\d*)/$', topic_views.display_topic),
    # post a topic
    url(r'^posttopic/$', topic_views.post_topic),
    # reply a topic
    url(r'^reply/$', topic_views.reply_topic),
    # vote a topic
    url(r'^vote/$', topic_views.vote_topic),
    url(r'^favtopic/$', topic_views.fav_topic),
    url(r'^delete/$', topic_views.delete_topic),
    url(r'^settop/$', topic_views.set_topic_top),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#TODO do not use this in a production enviroment