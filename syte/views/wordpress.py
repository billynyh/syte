# -*- coding: utf-8 -*-
import os
from datetime import datetime

import requests
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from pybars import Compiler

def wordpress(request):
    r = requests.get('{0}/get_recent_posts?'.format(settings.WORDPRESS_API_URL))
    return HttpResponse(content=r.text, status=r.status_code, 
        content_type=r.headers['content-type'])

def wordpress_post(request, post_id):
    context = dict()

    r = requests.get('{0}/get_post/?post_id={1}'.format(
        settings.WORDPRESS_API_URL, post_id))
    if r.status_code == 200:
        post_response = r.json

        path = '{0}/static/templates/wordpress-post.html'.format(
            os.path.join(os.path.dirname(__file__), '..'))
        with open(path, 'r') as f:
            f_data = f.read()

        compiler = Compiler()
        template = compiler.compile(unicode(f_data))
        
        post = post_response.get("post", {})
        f_date = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')
        post['formated_date'] = f_date.strftime('%B %d, %Y')

        context['post_data'] = template(post)
        context['post_title'] = post.get('title', None)
    
    return render(request, 'blog-post.html', context)
