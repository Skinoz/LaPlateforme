import { ref } from 'vue'

export interface NIC {
  IP: string;
  MAC: string;
  NETWORK: string;
  NETWORK_ID: string;
  NIC_ID: string;
  SECURITY_GROUPS: string;
}

export interface DISK {
  DISK_ID: string;
  DATASTORE: string;
  DATASTORE_ID: string;
  IMAGE: string;
  IMAGE_ID: string;
  SIZE: string;
  TYPE: string;
  CLONE: string;
  CLONE_TARGET: string;
  LN_TARGET: string;
  DISK_SNAPSHOT_TOTAL_SIZE: string;
}

export interface GRAPHICS {
  LISTEN: string;
  PORT: string;
  TYPE: string;
}

export interface Template {
  CPU: string;
  MEMORY: string;
  VCPU: string;
  DISK: DISK;
  NIC: NIC | NIC[];
  GRAPHICS: GRAPHICS;
}

export interface VM {
  id: string;
  name: string;
  state: string;
  template: Template;
  active : boolean;
}

export interface Network {
  id: string;
  name: string;
  vms: VM[];
  active : boolean;
}

export const networkList = ref<Network[]>([])
export const vmList = ref<VM[]>([])
export const selectedNode = ref<VM | null>(null)
