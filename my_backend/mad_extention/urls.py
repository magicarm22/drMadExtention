from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'mad_extention'
urlpatterns = [
    path('info', views.UserInformation.as_view(), name='getUserInformation'),
    path('injection', views.StartInjection.as_view(), name='Injection'),
    path('health', views.Health.as_view(), name='Health'),
    path('shop', views.ShopCenter.as_view(), name='Shop'),
    path('inventory', views.MyInventory.as_view(), name='Inventory'),
    path('raids', views.RaidsInfo.as_view(), name='Raids')

]
