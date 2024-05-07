<template>
  <div class="h-full w-full absolute">
    <div v-if="showIframe" class="absolute inset-0 flex justify-center items-center">
      <div class="absolute inset-0 bg-gray-900 opacity-75"></div>
      <div class="relative z-10 w-full h-full">
        <div class="crop ratio ratio-16:9">
          <iframe :src="iframeSrc" ref="iframeRef" class="w-full h-full" style="border: none;"></iframe>
        </div>
        <div class="absolute top-0 right-0 m-2">
          <button @click="closeIframe" class="p-2 font-bold bg-red-500 text-white rounded-md ">X</button>
        </div>
      </div>
    </div>
  </div>
  <div class="flex">
    <div class="graph-container">
      <v-network-graph
        class="graph"
        :nodes="nodes"
        :edges="edges"
        :layouts="layouts"
        :configs="configs"
        :layers="layers"
        :eventHandlers="eventHandlers"
      >
      </v-network-graph>
    </div>
    <div class="bg-[#072637]">
      <div class="bg-[#051A26] border-2 p-4">
        <h1 class="font-semibold text-white w-40">VM List</h1>
      </div>
      <ul class="list-none">
        <li v-for="network in networkList" :key="network.id">
          <h2 class="text-white mt-4">{{ network.name }}</h2>
          <ul class="list-none">
            <li v-for="vm in network.vms" :key="vm.id" @click="selectNode(vm)" @dblclick="loadIframe(vm.id)">
              <p class="text-white my-2">{{ vm.name }}</p>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
  <div v-if="selectedNode" class="text-white p-4 absolute top-16 right-0 w-[20%] bg-[#051A26] h-[100%]">
    <div class="absolute top-0 right-0 m-2">
      <button @click="closeFrame" class="p-2 font-bold bg-red-500 text-white rounded-md">X</button>
    </div>
    <h2 class="font-semibold">Selected Node</h2>
    <p>ID: {{ selectedNode.id }}</p>
    <p>Name: {{ selectedNode.name }}</p>
    <p>State: {{ selectedNode.state }}</p>
    <p v-if="selectedNode.template">Template:</p>
    <ul v-if="selectedNode.template">
      <li>CPU: {{ selectedNode.template.CPU }}</li>
      <li>MEMORY: {{ selectedNode.template.MEMORY }}</li>
      <li>VCPU: {{ selectedNode.template.VCPU }}</li>
      <li v-if="Array.isArray(selectedNode.template.NIC)">
        NICs:
        <ul v-for="(nic, index) in selectedNode.template.NIC" :key="index">
          <li v-if="nic">
            <p>Network ID: {{ nic.NETWORK_ID }}</p>
            <p>IP: {{ nic.IP }}</p>
            <p>MAC: {{ nic.MAC }}</p>
            <p>NETWORK: {{ nic.NETWORK }}</p>
            <p>NIC ID: {{ nic.NIC_ID }}</p>
            <p>SECURITY GROUPS: {{ nic.SECURITY_GROUPS }}</p>
          </li>
        </ul>
      </li>
      <li v-else-if="selectedNode.template.NIC && typeof selectedNode.template.NIC === 'object'">
        <p>Network ID: {{ selectedNode.template.NIC.NETWORK_ID }}</p>
        <p>IP: {{ selectedNode.template.NIC.IP }}</p>
        <p>MAC: {{ selectedNode.template.NIC.MAC }}</p>
        <p>NETWORK: {{ selectedNode.template.NIC.NETWORK }}</p>
        <p>NIC ID: {{ selectedNode.template.NIC.NIC_ID }}</p>
        <p>SECURITY GROUPS: {{ selectedNode.template.NIC.SECURITY_GROUPS }}</p>
      </li>
    </ul>
    <p v-if="selectedNode.template">Graphics:</p>
    <ul v-if="selectedNode.template">
      <li>LISTEN: {{ selectedNode.template.GRAPHICS.LISTEN }}</li>
      <li>PORT: {{ selectedNode.template.GRAPHICS.PORT }}</li>
      <li>TYPE: {{ selectedNode.template.GRAPHICS.TYPE }}</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'
import { defineConfigs, EventHandlers } from 'v-network-graph'
import { ForceLayout, ForceNodeDatum, ForceEdgeDatum } from 'v-network-graph/lib/force-layout'

interface NIC {
  IP: string;
  MAC: string;
  NETWORK: string;
  NETWORK_ID: string;
  NIC_ID: string;
  SECURITY_GROUPS: string;
}

interface DISK {
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

interface GRAPHICS {
  LISTEN: string;
  PORT: string;
  TYPE: string;
}

interface Template {
  CPU: string;
  MEMORY: string;
  VCPU: string;
  DISK: DISK;
  NIC: NIC | NIC[];
  GRAPHICS: GRAPHICS;
}

interface VM {
  id: string;
  name: string;
  state: string;
  template: Template;
}

interface Network {
  id: string;
  name: string;
  vms: VM[];
}

function isNetworkNode (node: Network | VM): node is Network {
  return (node as Network).vms !== undefined
}

const configs = defineConfigs({
  view: {
    autoPanAndZoomOnLoad: 'fit-content',
    layoutHandler: new ForceLayout({
      positionFixedByDrag: false,
      positionFixedByClickWithAltKey: false,
      createSimulation: (d3, nodes, edges) => {
        const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
        const simulation = d3.forceSimulation(nodes)
          .force('edge', forceLink.distance(30).strength(1))
          .force('charge', d3.forceManyBody().strength(-2000))
          .force('x', d3.forceX())
          .force('y', d3.forceY())
          .tick(10)
        simulation.stop()
        return simulation
      }
    })
  },
  node: {
    selectable: true,
    scalingObjects: true,
    normal: {
      color: (n) => {
        const networkNode = n as unknown as Network | VM
        if (isNetworkNode(networkNode)) {
          return '#ff0000' // Red color for network nodes
        } else {
          return '#4466cc' // Blue color for VM nodes
        }
      }
    }
  }
})

export default {
  name: 'NetworkGraph',
  setup () {
    const networkList = ref<Network[]>([])
    const vmList = ref<VM[]>([])
    const selectedNode = ref<VM | null>(null)
    const iframeRef = ref<HTMLIFrameElement | null>(null)
    const showIframe = ref(false)
    const iframeSrc = ref('')

    onMounted(async () => {
      try {
        const [vmResponse, networkResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/v1/opennebula/vm-list/'),
          axios.get('http://localhost:8000/api/v1/opennebula/networks/')
        ])
        const vms: VM[] = vmResponse.data
        const networks: Network[] = networkResponse.data

        console.log('VMs:', vms)
        console.log('Networks:', networks)

        vmList.value = vms.map(vm => {
          return {
            ...vm,
            id: `vm-${vm.id}` // Prefixing VM ID with "vm-"
          }
        })
        console.log('VM List:', vmList.value)
        // Associate virtual machines with corresponding virtual networks
        networkList.value = networks.map(network => {
          const networkId = network.id
          const uniqueVMs = network.vms.map(vm => {
            return {
              ...vm,
              id: `vm-${vm.id}` // Prefixing VM ID with "vm-"
            }
          })
          return { ...network, id: `network-${networkId}`, vms: uniqueVMs } // Prefixing network ID with "network-"
        }).filter(network => network.vms.length > 0) // Show VM nodes only if there are VMs in the network
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    })

    const nodes = computed(() => {
      const nodeMap: Record<string, Network | VM> = {}
      networkList.value.forEach(network => {
        nodeMap[network.id] = network
        network.vms.forEach(vm => {
          nodeMap[vm.id] = vm
        })
      })
      console.log('NodesMap:', nodeMap) // Log the nodeMap
      return nodeMap
    })

    const edges = computed(() => {
      let edgeIndex = 1
      const edgeMap: Record<string, { source: string; target: string }> = {}
      networkList.value.forEach(network => {
        network.vms.forEach(vm => {
          edgeMap[`edge${edgeIndex}`] = { source: network.id, target: vm.id }
          edgeIndex++
        })
      })
      console.log('Edges:', edgeMap) // Log the edgeMap

      return edgeMap
    })

    const layouts = computed(() => {
      const networkCount = networkList.value.length
      console.log('Network Count:', networkCount)
      const networkLayouts: Record<string, { x?: number; y?: number; fixed: boolean }> = {}
      const radius = 250
      const centerX = 200 // Adjust as necessary
      const centerY = 200 // Adjust as necessary
      vmList.value.forEach((vm, index) => {
        const savedPosition = localStorage.getItem(`${vm.id}-position`)
        if (savedPosition) {
          networkLayouts[vm.id] = JSON.parse(savedPosition)
          networkLayouts[vm.id].fixed = true
        } else {
          const angle = (index / networkCount) * 2 * Math.PI
          const x = undefined
          const y = undefined
          networkLayouts[vm.id] = { x, y, fixed: true }
        }
      })
      networkList.value.forEach((network, index) => {
        const savedPosition = localStorage.getItem(`${network.id}-position`)
        if (savedPosition) {
          networkLayouts[network.id] = JSON.parse(savedPosition)
          networkLayouts[network.id].fixed = true
        } else {
          const angle = (index / networkCount) * 2 * Math.PI
          const x = centerX + radius * Math.cos(angle)
          const y = centerY + radius * Math.sin(angle)
          networkLayouts[network.id] = { x, y, fixed: true }
        }
      })
      console.log('Network Layout :', networkLayouts)
      return { nodes: networkLayouts }
    })

    const layers = {
      badge: 'nodes'
    }

    const eventHandlers: EventHandlers = {
      'node:click': ({ node }) => {
        selectedNode.value = nodes.value[node] as VM
      },
      'node:dblclick': ({ node }) => {
        const vm = nodes.value[node] as VM
        loadIframe(vm.id)
      },
      'node:dragend': (event) => {
        Object.keys(event).forEach(key => {
          console.log(key, event[key])
          if (event[key]) {
            localStorage.setItem(`${key}-position`, JSON.stringify(event[key]))
          }
        })
      }
    }

    const closeFrame = () => {
      selectedNode.value = null
    }

    const selectNode = (vm: VM) => {
      selectedNode.value = vm
    }

    const loadIframe = (vmId: string) => {
      const id = vmId.split('-')[1] // Extract id from "vm-[id]"
      // Request the JWT
      axios.post('http://localhost:8000/api/v1/opennebula/token/', { username: 'oneadmin', password: process.env.VUE_APP_PASSWORD_OPENNEBULA })
        .then(response => {
          console.log('token:', response.data.token) // Get the JWT token from the backend
          // Show the iframe
          showIframe.value = true
          iframeSrc.value = `http://192.168.1.1:2616/fireedge/sunstone/guacamole/${id}/vnc?externalToken=${response.data.token}`
          nextTick(() => {
            iframeRef.value?.focus()
          })
        })
        .catch(error => {
          console.error('Error while getting JWT:', error)
        })
    }

    const closeIframe = () => {
      showIframe.value = false
      iframeSrc.value = ''
    }

    return {
      nodes,
      edges,
      layouts,
      configs,
      layers,
      eventHandlers,
      networkList,
      selectedNode,
      showIframe,
      closeFrame,
      selectNode,
      loadIframe,
      closeIframe,
      iframeSrc,
      iframeRef
    }
  }
}
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: calc(100vh - 70px); /* 70px is the height of the navigation bar */
  display: flex;
  justify-content: center; /* Horizontally center */
  align-items: center; /* Vertically center */
}

.graph {
  width: 100%; /* Use full width of parent */
  height: 100%; /* Use full height of parent */
  max-width: 100%; /* Do not exceed parent's width */
  max-height: 100%; /* Do not exceed parent's height */
}

/* Ajoutez votre style ici si nécessaire */
.box {
  margin: 3em auto;
  overflow: hidden;
  width: 250px;
}

.ratio {
  position: relative;
}

.ratio::before {
  background: rgba(0,0,0,.5);
  color: white;
  display: block;
  left: 0;
  padding: .25em;
  position: absolute;
  top: 0;
  z-index: 10;
}

.ratio-16\:9 { padding-top: 56.25%; }

.crop {
  background: black;
  overflow: hidden;
  position: relative;
}

.crop > * {
  height: 100%;
  left: 50%;
  position: absolute;
  transform: translateX(-50%) translateY(-50%);
  top: 50%;
  right: -50%;
}
</style>
