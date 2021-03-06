"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login',views.login),
    path('signup',views.signup),
    path('signupauth',views.signupIndex),
    path('', views.index),
    path('main', views.main),
    path('test',views.Reservation.as_view()),
    path('alarm',views.Alarm.as_view()),
    path('signal',views.Sendsignal.as_view()),
    path('foo',views.foo),
    path('signaltest',views.signaltest),
    path('logout',views.logout),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
