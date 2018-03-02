# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from .models import IMG
from .zmq_detector import ZmqDetector
from django.views.decorators.csrf import csrf_exempt
import urllib
import json
import os
from .tasks import add
from urllib.parse import unquote
# import the logging library
# import logging
#
# # Get an instance of a logger
# logger = logging.getLogger(__name__)




detector = ZmqDetector()
# Create your views here.
def index(request):
    add.delay(2,2)
    return HttpResponse("API")

@csrf_exempt
def detect(request):
    if request.method == "POST":
        url = unquote(request.POST["url"])
        path = os.path.join(settings.DETECT_IMAGE_ROOT, os.path.split(url)[-1]) # 图片的绝对路径

        # 为了统一组织图片存储，不允许检测非本机的图片。待检测图片必须为通过uploadImg上传的图片。
        # host, img_path = urllib.splithost(urllib.splittype(url)[1])
        # # 如果url为本机的图片，则直接获取文件路径进行识别
        # if host == request.get_host():
        #     path = img_path[1:]
        # else:
        #     print('NOT HOST')
        #     urllib.urlretrieve(url, path)
        # 直接使用request的id做为zmq的id
        result = detector.detect(path, str(id(request)))
        # logger.warning(result)
        return HttpResponse(result, content_type="application/json")
    return HttpResponseBadRequest(HttpResponse('请求非法'))

@csrf_exempt
def uploadImg(request):

    return render(request, 'uploadimg.html')

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
        return HttpResponse('http://' + request.get_host() + new_img.img.url)
    else:
        return HttpResponseBadRequest(HttpResponse('请求非法'))


@csrf_exempt
def upload_and_detect(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
        path = "media/img/" + new_img.name
        result = detector.detect(path, str(request.session.session_key))
        # print(result)
        return HttpResponse(result, content_type="application/json")
    else:
        return HttpResponse('Error')
