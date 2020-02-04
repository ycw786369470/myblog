from threading import Thread
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from device_manage.New_built_view import New_Built_View
from device_manage.models import *
import datetime
from django.http import JsonResponse
import hashlib
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.generic import ListView
from utils import constants
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from device_manage import init_start
import time
import json
import os
import math


# 给管理员发送邮件
def send_admin(to_email, name, start_time):
    subject = '需求发布信息'
    message = ''
    from_email = settings.EMAIL_FROM
    receiver = to_email
    html_message = '<h2>管理员，您好！ {} 在{}发布了新的需求</h2>请点击下面的链接进行登录查看:<br/>' \
                   '<a href = "http://127.0.0.1:8000/">http://127.0.0.1:8000/</a>'.format(name,start_time)
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=receiver,html_message=html_message)


# 给测试员发送邮件
def send_csy(to_email, name):
    subject = '任务分配信息'
    message = ''
    from_email = settings.EMAIL_FROM
    receiver = to_email
    html_message = '<h2> {} 您好！您有新的测试任务了</h2>请点击下面的链接进行登录查看:<br/>' \
                   '<a href = "http://127.0.0.1:8000/">http://127.0.0.1:8000/</a>'.format(name)
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=receiver,
              html_message=html_message)


# 筛选非空值或float
def get_value(value):
    if len(value) == 0:
        return 0
    elif value == '' or value == ' ':
        return 0
    elif value == 'none':
        return 0
    else:
        return value


# 保存用户记录
def save_action(request, txt):
    name = request.session.get('name')
    action = UserActionRecord()
    action.user = User.objects.get(name=name)
    action.time = datetime.datetime.now()
    action.action = txt
    action.save()


# 监听待分配的需求
def check_allotted(request):
    not_allotted = TestRequirements.objects.filter(is_finished=None).count()
    return HttpResponse(not_allotted)

