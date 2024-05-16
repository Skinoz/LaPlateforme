<template>
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
          <template #badge="{ scale }">
            <circle
              v-for="(pos, node) in layouts.nodes"
              :key="node"
              :cx="pos.x + 9 * scale"
              :cy="pos.y - 9 * scale"
              :r="4 * scale"
              :fill="getNodeColor(node)"
            />
          </template>
        </v-network-graph>
    </div>
  </div>
  <SideGraphMenu :nodeId="selectedNode?.id || ''"/>
  <VmIframe :iframeSrc="iframeSrc" :showIframe="showIframe"/>
</template>

<script lang="ts">
import { VM, Network, networkList, selectedNode, vmList } from '@/interfaces/NebulaInterface'
import { loadIframe, iframeSrc, showIframe } from '@/actions/IframeAction'
import SideGraphMenu from '@/components/Menus/NebulaMenu/SideGraphMenu.vue'
import VmIframe from '@/components/view/VmIframe.vue'
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { defineConfigs, EventHandlers } from 'v-network-graph'
import { ForceLayout, ForceNodeDatum, ForceEdgeDatum } from 'v-network-graph/lib/force-layout'

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
    label: {
      visible: true,
      direction: 'south',
      directionAutoAdjustment: true
    },
    normal: {
      type: 'rect',
      width: 32,
      height: 32,
      borderRadius: 6,
      strokeWidth: 1,
      strokeColor: '#888888',
      color: (n) => {
        const networkNode = n as unknown as Network | VM
        if (isNetworkNode(networkNode)) {
          return '#e73e01' // Red color for network nodes
        } else {
          return '#74d0f1' // Blue color for VM nodes
        }
      }
    },
    hover: {
      color: (n) => {
        const networkNode = n as unknown as Network | VM
        if (isNetworkNode(networkNode)) {
          return '#e9511a' // Red color for network nodes
        } else {
          return '#81D4F2' // Blue color for VM nodes
        }
      }
    }
  }
})

export default {
  name: 'TestComponent',
  components: {
    SideGraphMenu,
    VmIframe
  },
  setup () {
    const layoutNodes: Record<string, { x: number; y: number; fixed?: boolean }> = {}
    const layouts = ref({ nodes: layoutNodes })
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
              id: `vm-${vm.id}`, // Prefixing VM ID with "vm-"
              active: false
            }
          })
          return { ...network, id: `network-${networkId}`, vms: uniqueVMs } // Prefixing network ID with "network-"
        }).filter(network => network.vms.length > 0) // Show VM nodes only if there are VMs in the network
        setLayoutPositions()
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    })

    function isVMNode (nodeId: string) {
      const vm = vmList.value.find(vm => vm.id === nodeId)
      return vm !== undefined
    }

    const nodes = computed(() => {
      const nodeMap: Record<string, Network | VM> = {}
      networkList.value.forEach(network => {
        nodeMap[network.id] = network
        network.vms.forEach(vm => {
          nodeMap[vm.id] = vm
        })
      })
      console.log('NodesMap:', nodeMap)
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

    const setLayoutPositions = () => {
      const radius = 250
      const centerX = 0
      const centerY = 0

      vmList.value.forEach((vm, index) => {
        const savedPosition = localStorage.getItem(`${vm.id}-position`)
        if (savedPosition) {
          layoutNodes[vm.id] = JSON.parse(savedPosition)
          layoutNodes[vm.id].fixed = true
        } else {
          const x = vmList.value.length > 1 ? centerX + radius * Math.cos((index / vmList.value.length) * 2 * Math.PI) : 0
          const y = vmList.value.length > 1 ? centerY + radius * Math.sin((index / vmList.value.length) * 2 * Math.PI) : 0
          layoutNodes[vm.id] = { x, y, fixed: undefined }
        }
      })

      networkList.value.forEach((network, index) => {
        const savedPosition = localStorage.getItem(`${network.id}-position`)
        if (savedPosition) {
          layoutNodes[network.id] = JSON.parse(savedPosition)
          layoutNodes[network.id].fixed = true
        } else {
          const angle = (index / networkList.value.length) * 2 * Math.PI
          const x = centerX + radius * Math.cos(angle)
          const y = centerY + radius * Math.sin(angle)
          layoutNodes[network.id] = { x, y, fixed: true }
        }
      })

      layouts.value = { nodes: layoutNodes }
      console.log('Layottuts:', layouts.value)
    }

    onMounted(setLayoutPositions)

    const layers = {
      badge: 'nodes'
    }

    const eventHandlers: EventHandlers = {
      'view:click': () => {
        selectedNode.value = null
      },
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
            const vm = vmList.value.find(vm => vm.id === key)
            if (vm) {
              layoutNodes[vm.id] = { x: event[key].x, y: event[key].y, fixed: true }
            }
          }
        })
      },
      'node:pointermove': (event) => {
        Object.keys(event).forEach(key => {
          console.log(key, event[key])
          if (event[key]) {
            const vm = vmList.value.find(vm => vm.id === key)
            if (vm) {
              layoutNodes[vm.id] = { x: event[key].x, y: event[key].y, fixed: true }
            }
          }
        })
      }
    }

    const layoutsText = computed(() => {
      console.log('layouts:', layouts.value)
      return JSON.stringify(layouts.value, null, 2)
    })

    const getNodeColor = (nodeId: string) => {
      const vm = vmList.value.find(vm => vm.id === nodeId)
      if (!vm) return 'none'
      const state = parseInt(vm.state)
      if (state === 8) {
        return '#ff0000' // Rouge
      } else if (state === 1) {
        return '#ff9900' // Orange
      } else if (state === 3) {
        return '#00A300' // Vert
      } else {
        return '#044B9466' // Bleu
      }
    }

    const closeFrame = () => {
      selectedNode.value = null
    }

    const selectNode = (vm: VM) => {
      selectedNode.value = vm
    }

    const isVMActive = (nodeId: string) => {
      const vm = vmList.value.find(vm => vm.id === nodeId)
      if (vm === undefined) return false
      const state = parseInt(vm.state || '0')
      let isActive = false
      if (state === 3) {
        isActive = true
      } else {
        isActive = false
      }
      console.log(isActive)
      return isActive
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
      closeFrame,
      selectNode,
      isVMActive,
      isVMNode,
      isNetworkNode,
      layoutsText,
      getNodeColor,
      iframeSrc,
      showIframe
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
</style>
