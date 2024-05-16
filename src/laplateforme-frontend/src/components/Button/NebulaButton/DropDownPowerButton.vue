<template>
  <div class="relative" @click="isOpen = !isOpen">
    <button class="p-2 font-bold bg-blue-500 text-white rounded-md">
      Power
    </button>
    <div v-show="isOpen" class="absolute right-0 mt-2 w-32 bg-white border border-gray-200 divide-y divide-gray-100 rounded-md shadow-lg">
      <a @click="poweroff" v-if="selectedNode.state == '3'" class="cursor-pointer block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Power Off</a>
      <a @click="reboot" v-if="selectedNode.state == '3'" class="cursor-pointer block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Reboot</a>
      <a @click="poweron" v-if="selectedNode.state == '8'" class="cursor-pointer block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Power On</a>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { selectedNode, vmList } from '@/interfaces/NebulaInterface'
import axios from 'axios'

export default defineComponent({
  setup () {
    const isOpen = ref(false)

    const poweroff = () => {
      console.log('Poweroff')
      const token = localStorage.getItem('token')
      // API call to logout with djoser endpoint
      const id = selectedNode.value?.id.split('-')[1]

      axios
        .post(process.env.VUE_APP_PROTOCOL + '://' + process.env.VUE_APP_HOST_BACKEND_SERVER + ':' + process.env.VUE_APP_PORT + '/api/v1/opennebula/poweroff/', { vm: id })
        .then((request) => {
          if (request.status === 200) {
            const vm = vmList.value.find(vm => vm.id === selectedNode.value?.id)
            if (vm === undefined) return
            vm.state = '8'
            if (selectedNode.value) {
              selectedNode.value.state = '8'
            }
          }
          console.log('request sent', request)
        })
      console.log(token)
    }

    const poweron = () => {
      console.log('poweron')
      const token = localStorage.getItem('token')
      // API call to logout with djoser endpoint
      const id = selectedNode.value?.id.split('-')[1]

      axios
        .post(process.env.VUE_APP_PROTOCOL + '://' + process.env.VUE_APP_HOST_BACKEND_SERVER + ':' + process.env.VUE_APP_PORT + '/api/v1/opennebula/poweron/', { vm: id })
        .then((request) => {
          if (request.status === 200) {
            const vm = vmList.value.find(vm => vm.id === selectedNode.value?.id)
            if (vm === undefined) return
            vm.state = '3'
            if (selectedNode.value) {
              selectedNode.value.state = '3'
            }
          }
          console.log('request sent', request)
        })
      console.log(token)
    }

    const reboot = () => {
      console.log('reboot')
      const token = localStorage.getItem('token')
      // API call to logout with djoser endpoint
      const id = selectedNode.value?.id.split('-')[1]

      axios
        .post(process.env.VUE_APP_PROTOCOL + '://' + process.env.VUE_APP_HOST_BACKEND_SERVER + ':' + process.env.VUE_APP_PORT + '/api/v1/opennebula/reboot/', { vm: id })
        .then((request) => {
          if (request.status === 200) {
            const vm = vmList.value.find(vm => vm.id === selectedNode.value?.id)
            if (vm === undefined) return
            vm.state = '3'
            if (selectedNode.value) {
              selectedNode.value.state = '3'
            }
          }
          console.log('request sent', request)
        })
      console.log(token)
    }

    return {
      selectedNode,
      reboot,
      poweron,
      poweroff,
      isOpen
    }
  }
})
</script>

<style scoped>
/* Add your styles here */
</style>
