from django.urls import path
from . import views
from .token import Token

urlpatterns = [
    path('vm-list/', views.get_vm_list, name='get_vm_list'),
    path('token/', Token.as_view(), name='get_auth_token'),
    # You can add more endpoints here
]
