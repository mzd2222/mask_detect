from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class feedbacks(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    feedback_msg = models.CharField(max_length=100, null=False)
    feedback_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feedbacks_table"


class comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    feedback = models.ForeignKey(feedbacks, on_delete=models.CASCADE, null=False)
    comment_msg = models.CharField(max_length=100)
    comment_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments_table"
