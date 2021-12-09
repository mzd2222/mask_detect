from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# 用户剩余资源
class User_resources(models.Model):
    resource_table_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    img_nums = models.IntegerField(default=0, null=False)
    camera_nums = models.IntegerField(default=0, null=False)
    video_nums = models.IntegerField(default=0, null=False)

    class Meta:
        db_table = "User_resources_table"


# 已部署摄像头信息
class Camera(models.Model):
    camera_id = models.AutoField(primary_key=True)
    camera_name = models.CharField(max_length=30, null=False)
    # used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    desc = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "Camera_msg_table"
