from django.urls import path,re_path

from . import consumer

websocket_urlpatterns = [
    #  path('ws/chat/<str:room_name>/$', consumer.ChatConsumer),
     re_path(r'^ws/chat/(?P<room_name>[^/]+)/$',consumer.ChatConsumer)
]