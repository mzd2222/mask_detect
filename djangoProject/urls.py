"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from login_register import views as login_register_views
from feedback import views as feedback_views
from mask_detect import views as mask_detect_views

urlpatterns = [

    path('video/', include('video.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),

    # login_register
    path('login_register/register/', login_register_views.register),
    path('login_register/login/', login_register_views.login),
    path('login_register/logout/', login_register_views.logout),

    # feedback_comment
    path('feedback/create_feedback/', feedback_views.Create_feedback),
    path('feedback/create_comment/', feedback_views.Create_comment),


    # mask_detect
    path('mask_detect/create_camera/', mask_detect_views.Create_camera),
    path('mask_detect/get_user_resources/', mask_detect_views.Get_User_resources),
    path('mask_detect/get_camera/', mask_detect_views.Get_Camera),
    path('mask_detect/user_add_camera/', mask_detect_views.User_add_Camera),
    path('mask_detect/add_user_resources/', mask_detect_views.Add_User_resources),
    path('mask_detect/picture_calculate/', mask_detect_views.Picture_calculate),
    path('mask_detect/video_calculate/', mask_detect_views.Video_calculate),
    path('mask_detect/video_get/', mask_detect_views.Video_get),
]
