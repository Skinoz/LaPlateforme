import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from pyone import OneServer

url = f"{os.environ.get('PROTOCOL')}://{os.environ.get('IP_SERVER')}:{os.environ.get('API_PORT')}/RPC2"
one = OneServer(url, session="oneadmin:Gtxt4mLMSKJKQLAeKyFQ")

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def poweroff(request):
    vm_id = request.data.get('vm')
    id = int(vm_id)
    print(f"PowerOffVm: {vm_id}")
    try:
        one.vm.action("poweroff-hard", id)
        return Response({'message': 'VM powered off'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"[Exception] : {e}")
        return Response({'error': 'Failed to power off VM'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def poweron(request):
    vm_id = request.data.get('vm')
    id = int(vm_id)
    print(f"PowerOnVm: {vm_id}")
    try:
        one.vm.action("resume", id)
        return Response({'message': 'VM powered on'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"[Exception] : {e}")
        return Response({'error': 'Failed to power on VM'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reboot(request):
    vm_id = request.data.get('vm')
    id = int(vm_id)
    print(f"RebootVm: {vm_id}")
    try:
        one.vm.action("reboot", id)
        return Response({'message': 'VM reboot'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"[Exception] : {e}")
        return Response({'error': 'Failed to reboot VM'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)