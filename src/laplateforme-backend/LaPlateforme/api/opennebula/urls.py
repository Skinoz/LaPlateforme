from django.urls import path
from . import views, token

urlpatterns = [
    path('vm-list/', views.get_vm_list, name='get_vm_list'),
    path('networks/', views.get_network_list, name='get_network_list'),
    path('token/', token.get_token, name='get_token'),
    # You can add more endpoints here
]
