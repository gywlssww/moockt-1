from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.conf import settings
from django.urls import reverse

from moocacha import views

from chatbot.models import ChatbotUser

import socket
import requests
import json
import os.path

address = "114.70.21.89"
PORT1 = 9005 #AIML
PORT2 = 9006 #Dialogflow
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })

def chkTime(mystr):
    if len(mystr)==0:
        return "e"
    sft_time = mystr
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
    
    #cmd msg
    if len(return_str)!=0 and return_str[0] == '!':

        try:
            ChatbotUser.objects.get(user_id=return_id)
        except ChatbotUser.DoesNotExist:
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
        if return_str == "!session":
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

        sft_time = chkTime(return_str[1:])

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
            if sft_time=="재생":
                post_data = {"message":return_id,'shifted':0,'op':'play'}
                response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "동영상 재생"
                            }
                        }],
                    }
                })
            
            elif sft_time=="정지":
                post_data = {"message":return_id,'shifted':0,'op':'stop'}
                response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "동영상 일시정지"
                            }
                        }],
                    }
                })
            elif sft_time=="다음":
                post_data = {"message":return_id,'shifted':0,'op':'next'}
                response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "다음 동영상"
                            }
                        }],
                    }
                })
            elif sft_time=="음소거":
                post_data = {"message":return_id,'shifted':0,'op':'mute'}
                response = requests.post('http://localhost:8000/signal', data=json.dumps(post_data))
                return JsonResponse({
                    'version': "2.0",
                    'template': {
                        'outputs': [{
                            'simpleText': {
                                'text': "동영상 음소거"
                            }
                        }],
                    }
                })    
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

    requestMsg = json.dumps(return_str) + "\n"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, PORT1))
            s.sendall(requestMsg.encode("utf-8"))
            received = str(s.recv(1024), "utf-8")

    except socket.error as e:
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "잘못된 입력 또는 챗봇이 꺼져있음"
                    }
                }],
            }
        })
    print("R: "+received)
    if received == "해당되는 내용이 없습니다.":
        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #         s.connect((address, PORT2))
        #         s.sendall(requestMsg.encode("utf-8"))
        #         received = str(s.recv(1024), "utf-8")
        
        # except socket.error as e:
        #     return JsonResponse({
        #         'version': "2.0",
        #         'template': {
        #             'outputs': [{
        #                 'simpleText': {
        #                     'text': "잘못된 입력 또는 챗봇이 꺼져있음"
        #                 }
        #             }],
        #         }
        #     })


        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [
                    {
                        "simpleText":{
                            "text":"적절한 응답을 찾지 못했습니다. 게시판에 등록하시겠습니까?"
                        }
                    }
                ],

                "quickReplies": [
                    {
                        'label':"직접 질문",
                        'action':'message',
                        'messageText':"직접 질문"
                    },
                    {
                        'label':"게시판에 등록",
                        'action':'message',
                        'messageText':"게시판에 등록"
                    }
                ]
            }
        })
    
    return JsonResponse({
        'version': "2.0",
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': received
                }
            }],
        }
    })
    
def shiftedpage(request):
    data = dict()
    return render(request, 'chatbot/main.html',data)
