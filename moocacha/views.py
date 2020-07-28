from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.conf import settings
import threading
import datetime
import json
import os
import socket
import requests
#from .forms import *
#from . import gcpapi

#media files
video_file_path = os.path.join(settings.MEDIA_ROOT, 'video/')
audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio/')
script_file_path = os.path.join(settings.MEDIA_ROOT, 'script/')
aiml_file_path = os.path.join(settings.MEDIA_ROOT, 'aiml/')
thumb_file_path = os.path.join(settings.MEDIA_ROOT, 'thumbnail/')
data_file_path = os.path.join(settings.MEDIA_ROOT, 'chatbot_data/')
#BUCKET_NAME = settings.BUCKET_NAME

# broker PORT, IP
HOST = "114.70.21.90"
#HOST = "114.70.21.89"

PORT = 9009

# dictionary for chatbot info
chatbot_info = {}
# Create your views here.
#view of index page (main menu)
@csrf_exempt
def index(request):
    return render(request, 'moocacha/index.html')


#view of main page (video and chatbot)
@csrf_exempt
def main(request):
    data = dict()
    # blobs = gcpapi.list_blobs_with_prefix(BUCKET_NAME, 'video/')
    # video = settings.SAMPLE_VIDEO

    # if 'video' in request.GET.keys():
    #     video = request.GET['video']

    # data['videos'] = list()

    # for blob in blobs:
    #     name = blob.name.split('/')[-1]
    #     name = name.replace('\'', '')

    #     expiration = datetime.datetime.now()+datetime.timedelta(hours=1)

    #     if name != '' and name != video:
    #         meta = dict()
    #         meta['url'] = blob.generate_signed_url(expiration)
    #         meta['title'] = name
    #         data['videos'].append(meta)

    #     elif name == video:
    #         data['main_title'] = name
    #         data['main_url'] = blob.generate_signed_url(expiration)

    #     else:
    #         pass{
    #data['main_url'] =  "../media/video/Computing-thinking.mp4"
    return render(request, 'moocacha/main.html', data)

from django.views.generic import TemplateView
from . import models
import json
from django.shortcuts import HttpResponse
from .models import Test

class Alarm(TemplateView):
    template_name = "moocacha/main.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.username
        return context

class Reservation(TemplateView):
    template_name = "moocacha/test.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.username
        return context

    def post(self, request, **kwargs):
        ins=models.Test()
        data_unicode = request.body.decode('utf-8')
        data=json.loads(data_unicode)
        ins.message = data['message']
        ins.save()
        return HttpResponse('')

def signaltest(request):
    #data_unicode = request.body.decode('utf-8')
    #data = json.loads(data_unicode)
    data = dict()
    data['shifted'] = '500'
    data['op'] = 'plus'
    # data = {'shifted':'500','op':'plus'}
    return render(request,"moocacha/send-signal.html",data)

class Sendsignal(TemplateView):
    template_name = "moocacha/send-signal.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.username
        lastrecord = Test.objects.last()
        context['shifted'] = lastrecord.shifted
        context['op'] = lastrecord.op
        return context

    def post(self, request, **kwargs):
        
        ins=models.Test()
        data_unicode = request.body.decode('utf-8')
        data=json.loads(data_unicode)
        print(data)
        ins.message = data['message']
        ins.op = data['op']
        ins.shifted = data['shifted']
        ins.save()
        return HttpResponse('')

def foo(request):
    post_data = {'message': 'root','shifted':'500','op':'plus'}
    response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
    # content = response.content
    return HttpResponse(response)
