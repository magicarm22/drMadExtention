from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'mad_extention'
urlpatterns = [
    path('info', views.UserInformation.as_view(), name='getUserInfomation'),
    path('utils', views.Utils.as_view(), name='Utils'),
]