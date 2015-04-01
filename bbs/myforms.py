#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class signup_form(login_form):
    email = forms.CharField()
    #repassword = forms.CharField(widget=forms.PasswordInput)
    
class resetpwd_form(forms.Form):
    # old password
    old_password = forms.CharField(widget=forms.PasswordInput)
    # new password
    new_password = forms.CharField(widget=forms.PasswordInput)
    
class topic_form(forms.Form):
    # node id
    classify = forms.IntegerField()
    # title
    title = forms.CharField()
    # content
    content = forms.CharField()
   
class reply_form(forms.Form):
    # topic id
    topic_id = forms.IntegerField()
    # reply content
    content = forms.CharField()

class letter_form(forms.Form):
    from_username = forms.CharField()
    to_username = forms.CharField()
    content = forms.CharField()

class userinfo_form(forms.Form):
    screen_name =  forms.CharField(required = False)
    description =  forms.CharField(required = False)