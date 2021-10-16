from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    # 前端请求websocket连接
    path('wss/result/', consumers.SyncConsumer),
]