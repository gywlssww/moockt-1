
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('shiftedpage/', views.shiftedpage,name='shiftedpage'),
    url(r'shiftedpage',views.shiftedpage, name ='shiftedpage'),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
