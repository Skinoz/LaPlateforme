from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from pyone import OneServer
import os

url=f"{os.environ.get('PROTOCOL')}://{os.environ.get('IP_SERVER')}:{os.environ.get('API_PORT')}/RPC2"
one = OneServer(url, session="oneadmin:Gtxt4mLMSKJKQLAeKyFQ")

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_vm_list(request):
    # Récupération de la liste des machines virtuelles
    vms = one.vmpool.info(-1,-1,-1,-1).VM

    # Formatage des données
    vm_list = []
    for vm in vms:
        vm_info = {
            "id": vm.get_ID(),
            "name": vm.get_NAME(),
            "state": vm.get_STATE(),
            "template": vm.get_TEMPLATE()
        }
        vm_list.append(vm_info)

    return JsonResponse(vm_list, safe=False)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_network_list(request):
    # Récupération de la liste des réseaux virtuels
    networks = one.vnpool.info(-2, -1, -1).VNET
    vms = one.vmpool.info(-1,-1,-1,-1).VM

    # Formatage des données
    network_list = []
    for network in networks:
        network_info = {
            "id": network.get_ID(),
            "name": network.get_NAME(),
            "vms": []  # Liste des machines virtuelles associées à ce réseau
        }
        print("Network info ", network_info)
        for vm in vms:
            print("-------------------")
            print("VM Name ", vm.get_NAME())
            print("VM info ", vm.get_TEMPLATE())
            vm_template = vm.get_TEMPLATE()
            if vm_template and 'NIC' in vm_template:
                nics = vm_template['NIC']
                if isinstance(nics, list):  # Si plusieurs NICs
                    for nic in nics:
                        if 'NETWORK_ID' in nic and int(nic['NETWORK_ID']) == int(network.get_ID()):
                            vm_info = {
                                "id": vm.get_ID(),
                                "name": vm.get_NAME(),
                                "state": vm.get_STATE(),
                                "template": vm_template
                            }
                            network_info["vms"].append(vm_info)
                else:  # Si un seul NIC
                    if 'NETWORK_ID' in nics and int(nics['NETWORK_ID']) == int(network.get_ID()):
                        vm_info = {
                            "id": vm.get_ID(),
                            "name": vm.get_NAME(),
                            "state": vm.get_STATE(),
                            "template": vm_template
                        }
                        network_info["vms"].append(vm_info)

        network_list.append(network_info)

    print(network_list)
    return JsonResponse(network_list, safe=False)
