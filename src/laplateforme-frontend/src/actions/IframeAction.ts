import { ref } from 'vue'
import axios from 'axios'
import { vmList } from '@/interfaces/NebulaInterface'

export const iframeSrc = ref('')
export const showIframe = ref(false)

export const closeIframe = () => {
  showIframe.value = false
  iframeSrc.value = ''
}

export const loadIframe = (nodeId: string) => {
  const vm = vmList.value.find(vm => vm.id === nodeId)
  if (vm === undefined) return false
  const state = parseInt(vm?.state || '0')
  if (vmList.value.find(vm => vm.id === nodeId) === undefined) return // TODO ADD NOTIFICATION FOR USER
  if (state === 8) return // TODO ADD NOTIFICATION FOR USER

  console.log('VMINFO ON LOADIFRAME:', vm?.state)
  const id = nodeId.split('-')[1] // Extract id from "vm-[id]"
  // Request the JWT
  axios.post('http://localhost:8000/api/v1/opennebula/token/', { username: 'oneadmin', password: process.env.VUE_APP_PASSWORD_OPENNEBULA })
    .then(response => {
      console.log('token:', response.data.token) // Get the JWT token from the backend
      // Show the iframe

      showIframe.value = true
      iframeSrc.value = `http://192.168.1.1:2616/fireedge/sunstone/guacamole/${id}/vnc?externalToken=${response.data.token}`
    })
    .catch(error => {
      console.error('Error while getting JWT:', error)
    })
}
