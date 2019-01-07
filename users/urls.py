from django.conf.urls import url
from django.contrib.auth import login
from . import views

urlpatterns = [
    #Сторінка входу
    url(r'^login/$',login,name='login'),
    #Сторінка виходу
    url(r'^logout/$', views.logout_view, name='logout'),
]