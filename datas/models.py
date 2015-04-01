#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from bbs.myutils import  get_delta_time

class UserInfo(models.Model):
    # you can get userinfo like this: user.userinfo_set.all()[0]
    user = models.OneToOneField(User, primary_key=True)
    # path to avantar
    image = models.ImageField(upload_to='avatar', default='avatar/t_avatar.png')
    # description of user
    description = models.TextField(null=True, blank=True)
    # user's favorites
    fav = models.ManyToManyField('Topic', related_name= 'fav_user')
    # topic voted
    vote = models.ManyToManyField('Topic', related_name= 'vote_user')
    # coins of user
    coins = models.IntegerField(default=0)
    def __unicode__(self):
        return '<userInfo: %s>' % self.user
    def get_fav_topic(self):
        return self.fav.all()
    def get_fav_counts(self):
        return self.fav.count()
    def get_topic_count(self):
        return self.user.topics.filter(replys=None).count()
    def get_reply_count(self):
        return self.user.topics.exclude(replys=None).count()
    def get_unread_replys(self):
        all_replys = []
        for topic in self.user.topics.filter(is_active= True, replys=None):
            replys = Topic.objects.filter(replys= topic, is_read=False)
            for reply in replys:
                all_replys.append(reply)
        return all_replys        
# Topic model
class Topic(models.Model):
    # author of this topic
    user = models.ForeignKey(User, related_name='topics')
    # node the topic belong to
    node = models.ForeignKey('Node', related_name='topics')
    # title of this topic
    title = models.CharField(max_length=40, null=True, blank=True)
    # content of this topic
    content = models.TextField()
    # times people hits the topic
    hits = models.IntegerField(default=0)
    # the number of hitting like
    reply_count = models.IntegerField(default=0)
    # replys
    replys = models.ForeignKey('self',null = True, blank=True)
    # datetime created
    created = models.DateTimeField(auto_now_add=True)
    # datetime updated
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    # is active
    is_active = models.BooleanField(default=True)
    # is this reply read by author
    is_read = models.BooleanField(default=False)
    
    is_top = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '<Topic: %s>' % self.created
    # help to get user's avatar while showing topics in list
    def get_display_datetime(self):
        return get_delta_time(self.created)
    def get_reply_count(self):
        return Topic.objects.filter(replys=self, is_active=True).count()
    def get_last_reply(self):
        replys = Topic.objects.filter(replys=self, is_active=True).order_by('-created')
        return replys[0] if replys else None
    # if user read himself topic,all set all reply is read
    def set_is_read(self, user):
        if self.user==user:
            Topic.objects.filter(replys= self).update(is_read=True)
    class Meta:
        ordering = ['-created']
# nodes in homepage
class Node(models.Model):
    # node name
    title = models.CharField(max_length=40)
    # urlname todo:if it is need to save an url here or not
    # decription about the node
    description = models.TextField(null=True, blank=True)
    #
    role = models.CharField(max_length=20, null = True, blank=True)

    # topics will show on homepage ?
    on_home = models.BooleanField(default=False)
    # a mayor can delete a topic in this node, can change description
    mayor = models.ManyToManyField(User, related_name = 'mayors')
    # created time
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '<NodeTitle: %s>' % self.title
    
    
class Letter(models.Model):
    from_user = models.ForeignKey(User, related_name='letter_sended')
    to_user = models.ForeignKey(User, related_name='letter_received')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']