from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer),
    re_path(r'ws/test/(?P<username>.*)/',consumers.UserConsumer),
]
