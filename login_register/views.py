from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import auth
from login_register.models import *
import json
# Create your views here.
from mask_detect.models import *

@csrf_exempt
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        authority = request.POST.get('authority')

        print(username, password, email, authority, "注册")

        if not (username and password and email and authority):
            return JsonResponse({"state": "error", "msg": "msg_error"})

        Creat_user = User.objects.create_user(username=username, password=password,
                                                   email=email, is_staff=authority)

        if Creat_user:
            # return render(request, 'login/regist.html', {'registAdd': registAdd, 'username': username})
            User_resources.objects.create(user=Creat_user)
            return JsonResponse({"state": "ok", "msg": ""})
        else:
            # return render(request, 'login/classifacation.html', {'username': username})
            return JsonResponse({"state": "error", "msg": "msg_error"})

    else:
        print(request.method)
        return JsonResponse({"state": "method_error"})


@csrf_exempt
def login(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        # print(121)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)  # 用户认证
        if user is not None:  # 如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
            print("登录成功")
            auth.login(request, user)  # 登陆成功
            # return redirect('/', {'user': re})  # 跳转--redirect指从一个旧的url转到一个新的url
            # TODO: 返回msg信息由于user不可json化，看前端需要什么信息就返回什么信息，msg暂时为空
            return JsonResponse({"state": "ok", "msg": ""})
        else:  # 数据库里不存在与之对应的数据
            return JsonResponse({"state": "error", "msg": "login_error"})
    return JsonResponse({"state": "error", "msg": "method_error_repeat_login_error"})


@csrf_exempt
def logout(request):
    if request.method == "GET" and request.user.is_authenticated:
        auth.logout(request)
        return JsonResponse({"state": "ok", "msg": ""})
    else:
        return JsonResponse({"state": "error", "msg": "method_error repeat_logout"})
