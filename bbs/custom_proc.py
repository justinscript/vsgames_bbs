#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8
# define custom proc used by render_to_response
# use it like below:
# render_to_response('template_name', context_instance= RequestContext(request, processors=[functon_name_def_here]))
from datas.models import Topic, Node
from bbs.myutils import paging


# default context in main page
def cp_main_page(request):
    # get the announcement node
    try:
        ann = Node.objects.get(on_home=True)
    except Node.DoesNotExist:
        ann = None
    # get topics belongs to announcement
    n_list = Topic.objects.filter(node=ann, is_active=True)
    # get topics,exclude announcement
    node_title = request.GET.get('node')
    if node_title and Node.objects.filter(title=node_title).exists():
        t_list = Topic.objects.filter(replys = None, is_active=True, node=Node.objects.get(title=node_title)).order_by('-is_top', '-created')
    else:
        t_list = Topic.objects.filter(replys = None, is_active=True).exclude(node=ann)
    t_list = paging(request, t_list)
    # get nodes show on home page
    nodes = Node.objects.filter(on_home=False)
    # the main page always contain topics and announcement
    res = {
            'topic_list': t_list, 
            'ann_list': n_list,
            'nodes': nodes
            }
    return res

