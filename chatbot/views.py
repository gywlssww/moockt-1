from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.conf import settings
from django.urls import reverse

from moocacha import views

from chatbot.models import ChatbotUser

import requests
import json
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })

def chkTime(mystr):
    if len(mystr)==0:
        return "e"
    sft_time=""
    mystr = mystr.strip()
    lastchar = mystr[-1]
    if lastchar == '분':
        if len(mystr[:-1])>0 and mystr[:-1].isdigit():
            sft_time = int(mystr[:-1])*60
        else:
            sft_time = "e"            
    elif lastchar == '초':
        if len(mystr[:-1])>0 and mystr[:-1].isdigit():
            sft_time = int(mystr[:-1])
        else:
            sft_time = "e"
    elif lastchar == '뒤' or lastchar == '후':
        mystr = mystr[:-1].strip()
        sft_time = str(chkTime(mystr))+"+"
        
    elif lastchar == '전':
        mystr = mystr[:-1].strip()
        sft_time = str(chkTime(mystr))+"-"
    return str(sft_time)

@csrf_exempt
def message(request):
    data = dict()
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    return_id = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    
    if ChatbotUser.objects.get(user_id=return_id) == None:
        cu = ChatbotUser(user_id=return_id)
        cu.save()
        return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "발급받은 ID : {}".format(return_id)
                            }
                        }],
                    }
                })

    print(return_id)

    sft_time = chkTime(return_str)

    if len(sft_time)==0:
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "잘못된 입력"
                    }
                }],
            }           
        })
    else:
        if sft_time.isdigit():
            post_data = {'message': return_id,'shifted': sft_time ,'op': ''}
            response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
            return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "{}초로 이동".format(sft_time)
                        }
                    }],
                }
            })
        else:
            if sft_time[-1] == '+' and sft_time[:-1].isdigit():
                post_data = {'message': return_id,'shifted': sft_time[:-1],'op': 'plus'}
                response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "{}초 후로 이동".format(sft_time[:-1])
                            }
                        }],
                    }
                })
            elif sft_time[-1] == '-' and sft_time[:-1].isdigit():
                post_data = {'message': return_id,'shifted': sft_time[:-1],'op': 'minus' }
                response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "{}초 전으로 이동".format(sft_time[:-1])
                            }
                        }],
                    }
                })
            else:
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "잘못된 입력"
                            }
                        }],
                    }
                })


    if return_str == '5':
        data['shifted-time'] = 300
        print(data)
        #return render(request, 'moocacha/main.html', data)
        #return HttpResponseRedirect(reverse('shiftedpage'))

        post_data = {'message': 'root','shifted-time': '300'}
        response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))

        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "테스트 성공"
                    }
                }],
                'quictReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
            }
        })
    if return_str == '테스트':
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "테스트 성공"
                    }
                }],
                'quictReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
            }
        })
    
def shiftedpage(request):
    data = dict()
    return render(request, 'chatbot/main.html',data)
