from django.http import JsonResponse
from pyone import OneServer

def get_vm_list(request):
    # Connexion à l'hyperviseur OpenNebula
    one = OneServer("http://192.168.1.1:2633/RPC2", session="oneadmin:Gtxt4mLMSKJKQLAeKyFQ")

    # Récupération de la liste des machines virtuelles
    vms = one.vmpool.infoextended(-1,-1,-1,-1).VM

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
