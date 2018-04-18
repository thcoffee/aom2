from django.conf.urls import url
from django.conf.urls import  include, url  
from django.contrib.auth import views as views1
from . import views
urlpatterns = [
url('undo/', views.undo, name='undo'),
url('getdata/',views.getdata,name='getdata'),
url('putdata/',views.putdata,name='putdata'),
url('test/',views.test,name='test'),
url('dowarn/', views.dowarn, name='dowarn'),
url('review/', views.review, name='review'),
url('querywarn/', views.querywarn, name='querywarn'),
url('querywarninfo/', views.querywarninfo, name='querywarninfo'),
url('tjwarn/', views.tjwarn, name='tjwarn'),
]
