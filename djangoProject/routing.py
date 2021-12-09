# djangoProject/routing.py
# websocket的路由设置

from django.urls import re_path
import chat.consumers
import video.consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_name>\w+)/$', chat.consumers.ChatConsumer.as_asgi()),
    # re_path(r'video/(?P<v_name>\w+)/(?P<channel_name>\w+)/$', video.consumers.VideoConsumer.as_asgi())
    re_path(r'video/(?P<v_name>\w+)/$', video.consumers.VideoConsumer.as_asgi()),
]
