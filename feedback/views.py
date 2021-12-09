from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from feedback.models import *

# Create your views here.

@csrf_exempt
def Create_feedback(request):
    if request.method == "POST":
        feedback_msg = request.POST.get("feedback_msg")

        if not feedback_msg or not request.user.is_authenticated:
            return JsonResponse({"state": "error"})

        feedback_obj = feedbacks.objects.create(user=request.user,
                                                feedback_msg=feedback_msg)
        if not feedback_obj:
            JsonResponse({"state": "error"})

        print(request.user, "创建反馈：" + feedback_msg)
        return JsonResponse({"state": "ok"})
    return JsonResponse({"state": "error"})


@csrf_exempt
def Create_comment(request):
    if request.method == "POST":
        comment_msg = request.POST.get("comment_msg")
        feedback_id = request.POST.get("feedback_id")

        feedback_obj = feedbacks.objects.filter(feedback_id=feedback_id)

        # 检查权限 未登录
        if not request.user.is_authenticated:
            # or not (request.user.is_staff == 1 or request.user.id == feedback_obj.user.id):
            return JsonResponse({"state": "error"})

        # 检查数据
        if not feedback_obj or not comment_msg or not feedback_id:
            return JsonResponse({"state": "error"})

        feedback_obj = comments.objects.create(user=request.user,
                                               feedback=feedback_obj[0],
                                               comment_msg=comment_msg)
        if not feedback_obj:
            JsonResponse({"state": "error"})

        print(request.user, "评论: " + comment_msg)
        return JsonResponse({"state": "ok"})
    return JsonResponse({"state": "error"})
