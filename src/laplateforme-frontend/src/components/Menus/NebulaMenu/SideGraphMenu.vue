<template>
  <div >
    <div v-if="selectedNode && isVMNode(selectedNode.id)" class="text-white text-left p-4 absolute top-16 right-0 w-[20%] h-[calc(100vh-64px)] bg-[#051A26]">
      <div class="flex">
        <div class="m-2">
          <VmAccessButton @load-iframe="loadIframe" />
        </div>
        <div class="m-2">
          <DropDownPowerButton/>
        </div>
        <div class="m-2">
          <button @click="closeSideBar" class="p-2 font-bold bg-red-500 text-white rounded-md">X</button>
        </div>
      </div>
      <div class="grid grid-cols-2 border-white border-2 rounded p-4">
        <div>
          <p>Name: {{ selectedNode.name }}</p>
        </div>
      </div>
      <h2 class="font-semibold"></h2>
      <p>Name: {{ selectedNode.name }}</p>
      <p v-if="selectedNode.state">State: {{ selectedNode.state }}</p>
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
      <iframe
        v-if="showIframe"
        :src="iframeSrc"
        class="w-full h-full"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>
    <!-- NetworkInfo -->
    <div v-if="selectedNode && !isVMNode(selectedNode.id)" class="text-white text-left p-4 absolute top-16 right-0 w-[20%] bg-[#051A26] h-[100%]">
      <div class="absolute top-0 right-0 m-2">
        <button @click="closeFrame" class="p-2 font-bold bg-red-500 text-white rounded-md">X</button>
      </div>
      <h2 class="font-semibold">Selected Node</h2>
      <p>Name: {{ selectedNode.name }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { selectedNode, vmList } from '@/interfaces/NebulaInterface'
import VmAccessButton from '@/components/Button/NebulaButton/VmAccessButton.vue'
import DropDownPowerButton from '@/components/Button/NebulaButton/DropDownPowerButton.vue'

export default defineComponent({
  components: {
    VmAccessButton,
    DropDownPowerButton
  },
  props: {
    nodeId: {
      type: String,
      required: true
    }
  },
  setup (props: { nodeId: string }) {
    const isVMNode = (nodeId: string) => {
      const vm = vmList.value.find(vm => vm.id === nodeId)
      return !!vm
    }

    const closeSideBar = () => {
      selectedNode.value = null
    }

    const isVMActive = (nodeId: string) => {
      const vm = vmList.value.find(vm => vm.id === nodeId)
      if (vm === undefined) return false
      const state = parseInt(vm.state || '0')
      return state === 3
    }

    return {
      selectedNode,
      closeSideBar,
      isVMNode,
      isVMActive
    }
  }
})
</script>
