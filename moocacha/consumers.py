# -*- coding: utf-8 -*-

# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
#from . import gcpapi
#from .const import *

import json
import os
import socket
import pickle
import sys
#import aiml
import base64
import socket

#script file path
script_file_path = os.path.join(settings.MEDIA_ROOT, 'script/')

#Broker HOST, PORT
HOST = "114.70.21.89"
#HOST = "114.70.21.89"
PORT = 9009

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    #클라이언트로부터 메세지를 받을 시
    def receive(self, text_data):
        
        #dictionary for response
        response = dict()
        
        #사용자의 질문 메세지
        query_data_json = json.loads(text_data)
        print(text_data)
        # video title for finding script file for current video
        # video_title : list of video title and its format (format is not used so we throw it)
        video_title = query_data_json['videoName'].split('.')

        #user's question
        question = query_data_json['message']
        quest_time = query_data_json['time']
        total_time = query_data_json['totalTime']

        #sending user's question to broker
        data = dict()
        data["contents"] = question
        data["video_name"] = video_title[0]
        data["time"] = quest_time
        data["total_time"] = total_time
        
        #data has contents, video_name
        requestMsg = "/message?/" + json.dumps(data,ensure_ascii=False) + "\n"
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #챗봇과 연결
            s.connect((HOST, PORT))
            s.sendall(requestMsg.encode('utf-8'))
            received = str(s.recv(1024), "utf-8")

            #broker 동작

            #챗봇의 답 가져옴
            answer = json.loads(received.replace('\r\n', ''))
            s.close()

        response["message"] = 'Bot : ' + str(answer)
        response["timeShift"] = query_data_json['time']
        #print(response)
        self.send(json.dumps(response))


class Default_ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        #default chat
        text_data_json = json.loads(text_data)
        message = 'Bot : ' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import Test

@receiver(post_save, sender=Test)
def announce_stop(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "shares",{
                "type" : "share_message",
                "message" : instance.message,
                "shifted" :instance.shifted,
                "op" : instance.op
            }
        )
        
class UserConsumer(WebsocketConsumer):

    def connect(self):
        self.groupname="shares"
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
        )
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.groupname,
            self.channel_name
        )
    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        op = text_data_json['op']
        shifted = text_data_json['shifted']
        
        async_to_sync(self.channel_layer.group_send)(
            self.groupname,{
                'type': 'share_message',
                'message': message,
                'op': op,
                'shifted': shifted
            }
        )

    #recv msg from group
    def share_message(self,event):
        message = event['message']
        shifted = event['shifted']
        op = event['op']
        # send to ws
        self.send(text_data = json.dumps({
            'message': message,
            'shifted': shifted,
            'op': op

        }))