from django.urls import path
from . import views, token, power

urlpatterns = [
    path('vm-list/', views.get_vm_list, name='get_vm_list'),
    path('networks/', views.get_network_list, name='get_network_list'),
    path('token/', token.get_token, name='get_token'),
    path('poweroff/', power.poweroff, name='poweroff'),
    path('poweron/', power.poweron, name='poweron'),
    path('reboot/', power.reboot, name='reboot')
]
