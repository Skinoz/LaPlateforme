<template>
  <div>
    <div v-if="showIframe" class="fixed inset-0 flex justify-center items-center">
      <div class="absolute inset-0 bg-gray-900 opacity-75"></div>
      <div class="relative z-10 w-full h-full">
        <div class="h-full w-full">
          <iframe :src="iframeSrc" ref="iframeRef" class="fixed w-full h-full" frameborder="0" allowfullscreen @load="focusIframe"></iframe>
        </div>
        <div class="absolute top-0 right-0 m-2">
          <button @click="closeIframe" class="p-2 font-bold bg-red-500 text-white rounded-md">X</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { closeIframe } from '@/actions/IframeAction'

export default defineComponent({
  props: {
    iframeSrc: {
      type: String,
      required: true
    },
    showIframe: {
      type: Boolean,
      required: true
    }
  },
  setup (props) {
    const iframeRef = ref<HTMLIFrameElement | null>(null)

    const focusIframe = () => {
      iframeRef.value?.focus()
    }

    return {
      closeIframe: () => closeIframe(),
      iframeRef,
      focusIframe
    }
  }
})
</script>
