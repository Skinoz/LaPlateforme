<template>
  <button
    :disabled="!selectedNode || !isVMActive(selectedNode.id)"
    @click="!selectedNode || loadIframe(selectedNode?.id)"
    :class="{'bg-orange-500': !selectedNode || isVMActive(selectedNode?.id), 'bg-gray-600': !selectedNode || !isVMActive(selectedNode?.id)}"
    class="p-2 font-bold text-white rounded-md"
  >
  <svg style="filter: brightness(0) saturate(100%) invert(99%) sepia(42%) saturate(423%) hue-rotate(190deg) brightness(120%) contrast(100%);" height="30px" id="Layer_1" viewBox="0 0 48 48" width="30px"><path clip-rule="evenodd" d="M43,35H29.195c0.595,3.301,2.573,5.572,4.401,7H36c0.553,0,1,0.447,1,1  s-0.447,1-1,1H12c-0.553,0-1-0.447-1-1s0.447-1,1-1h2.403c1.827-1.428,3.807-3.699,4.401-7H5c-2.209,0-4-1.791-4-4V8  c0-2.209,1.791-4,4-4h38c2.209,0,4,1.791,4,4v23C47,33.209,45.209,35,43,35z M17.397,42h13.205c-1.595-1.682-3.015-3.976-3.459-7  h-6.287C20.412,38.024,18.992,40.318,17.397,42z M45,8c0-1.104-0.896-2-2-2H5C3.896,6,3,6.896,3,8v19l0,0h42V8z M45,29H3l0,0v2  c0,1.104,0.896,2,2,2h14l0,0h10l0,0h14c1.104,0,2-0.896,2-2V29z M24,32c-0.553,0-1-0.447-1-1s0.447-1,1-1s1,0.447,1,1  S24.553,32,24,32z" fill-rule="evenodd"/></svg>
  </button>
</template>

<script lang="ts">
import { selectedNode, vmList } from '@/interfaces/NebulaInterface'
import { iframeSrc, showIframe, loadIframe } from '@/actions/IframeAction'
import { ref, nextTick } from 'vue'

export default {
  props: {
    nodeId: {
      type: String,
      required: true
    }
  },
  setup (props: any, { emit }: any) {
    const iframeRef = ref<HTMLIFrameElement | null>(null)

    const isVMActive = (nodeId: string) => {
      const vm = vmList.value.find(vm => vm.id === nodeId)
      if (vm === undefined) return false
      const state = parseInt(vm.state || '0')
      return state === 3
    }

    return {
      selectedNode,
      showIframe,
      loadIframe,
      iframeSrc,
      isVMActive,
      iframeRef
    }
  }
}
</script>

<style scoped>
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

.crop {
  background: rgba(0,0,0,.5);
  overflow: hidden;
  position: relative;
}

.crop > * {
  height: calc(100%);
  left: 50%;
  position: absolute;
  transform: translateX(-50%) translateY(-50%);
  top: 50%;
  right: -50%;
}
</style>
