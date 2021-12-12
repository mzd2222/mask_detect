from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from .models import *
import cv2
import numpy as np
from yolov5 import mask_detect_img, mask_detect_video
import random
import datetime
import time
import json
import base64

def readFile(filename, chunk_size=1024):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# Create your views here.
def Get_User_resources(request):
    if not request.user.is_authenticated:
        # or not (request.user.is_staff == 1 or request.user.id == feedback_obj.user.id):
        return JsonResponse({"state": "error"})

    user_re_info = User_resources.objects.filter(user=request.user).values()[0]
    # print(user_re_info)

    return JsonResponse({"state": "ok", "resources": user_re_info})


def Get_Camera(request):
    if not request.method == 'GET':
        return JsonResponse({"state": "error"})

    user_Camera = []
    state = request.GET.get('state')

    # state == 0 表示获取未使用的相机
    if state == "0":
        user_Camera = Camera.objects.filter(user=None).values()
    # state == 1 表示获取用户的相机
    elif state == "1":
        user_Camera = Camera.objects.filter(user=request.user).values()

    cameras = []
    for i in user_Camera:
        cameras.append(i)
    cameras = json.dumps(cameras)

    return JsonResponse({"state": "ok", "cameras": cameras})


@csrf_exempt
def User_add_Camera(request):
    if not (request.user.is_authenticated and request.method == 'POST'):
        return JsonResponse({"state": "error"})

    user_resources = User_resources.objects.get(user=request.user)
    if user_resources.camera_nums < 1:
        return JsonResponse({"state": "no resources"})
    else:
        user_resources.camera_nums -= 1
        user_resources.save()

    camera_id = request.POST.get('camera_id')
    camera = Camera.objects.get(camera_id=camera_id)
    camera.user = request.user
    camera.save()

    return JsonResponse({"state": "ok"})


@csrf_exempt
def Create_camera(request):
    if not request.method == 'POST':
        return JsonResponse({"state": "error"})

    camera_name = request.POST.get('name')
    description = request.POST.get('description')
    creat_camera = Camera.objects.create(camera_name=camera_name, desc=description)

    if creat_camera:
        return JsonResponse({"state": "ok"})
    else:
        return JsonResponse({"state": "error"})


@csrf_exempt
def Add_User_resources(request):
    if not (request.user.is_authenticated and request.method == 'POST'):
        return JsonResponse({"state": "error"})

    state_code = request.POST.get('state_code')
    number = int(request.POST.get('number'))

    user_resources = User_resources.objects.get(user=request.user)

    if state_code == '0':
        user_resources.img_nums += number
    if state_code == '1':
        user_resources.camera_nums += number
    if state_code == '2':
        user_resources.video_nums += number

    user_resources.save()
    return JsonResponse({"state": "ok"})


@csrf_exempt
def Picture_calculate(request):
    if not (request.user.is_authenticated and request.method == 'POST'):
        return JsonResponse({"state": "error1"})

    user_resources = User_resources.objects.get(user=request.user)
    if user_resources.img_nums < 1:
        return JsonResponse({"state": "no resources"})
    else:
        user_resources.img_nums -= 1
        user_resources.save()

    file_obj = request.FILES.get('pic_file')
    if not file_obj:
        return JsonResponse({"state": "error2"})
    img = cv2.imdecode(np.array(bytearray(file_obj.read()), dtype='uint8'), cv2.IMREAD_UNCHANGED)
    frame, text = mask_detect_img.main_img(img)

    _, imgencode = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    data = np.array(imgencode)
    img = data.tobytes()
    img = base64.b64encode(img).decode()
    img = "data:image/jpg;base64," + img

    return JsonResponse({"image_data": img})

    # return HttpResponse(frame, content_type='image/jpg')
    # return JsonResponse({"state": "ok"})


@csrf_exempt
def Video_calculate(request):
    if not (request.user.is_authenticated and request.method == 'POST'):
        return JsonResponse({"state": "error"})

    user_resources = User_resources.objects.get(user=request.user)
    if user_resources.video_nums < 1:
        return JsonResponse({"state": "no resources"})
    else:
        user_resources.video_nums -= 1
        user_resources.save()

    file_obj = request.FILES.get('video_file')
    if not file_obj:
        return JsonResponse({"state": "error2"})
    video_name = 'static/videos/' + 'video_' + datetime.datetime.now().strftime(
        "%Y%m%d%H%M%S") + str(random.randint(1, 99)) + '.' + file_obj.name.split('.')[-1]
    with open(video_name, 'wb+') as f:
        f.write(file_obj.read())
    # print(video_name)
    video_name = video_name
    # print(video_name)
    video_path, text_path = mask_detect_video.main_video(video_name)
    # print(video_path, text_path)

    _, _, exp_path, video_path = video_path.split('\\')
    host = request.META['HTTP_HOST']

    download_path = host + '/mask_detect/video_get/?exp_path=' + exp_path + '&video_path=' + video_path

    return JsonResponse({"state": "ok", "url": download_path})


def Video_get(request):
    if not request.method == 'GET':
        return JsonResponse({"state": "error"})

    exp_path = request.GET.get('exp_path')
    video_path1 = request.GET.get('video_path')

    video_path = 'static/detect/' + exp_path + '/' + video_path1
    # print(video_path)
    file_name = video_path.split('/')[-1]
    response = StreamingHttpResponse(readFile(video_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

    return response
