<template>
  <div class="h-full w-full" style="position: relative;">
    <button @click="loadIframe">Accéder à la VM 12</button>
    <div v-if="showIframe" class="absolute inset-0 flex justify-center items-center">
      <div class="absolute inset-0 bg-gray-900 opacity-75"></div>
      <div class="relative z-10 w-full h-full">
        <div class="crop ratio ratio-16:9">
          <iframe ref="iframe" class="w-full h-full" style="border: none;"></iframe>
        </div>
        <div class="absolute top-0 right-0 m-2">
          <button @click="closeIframe" class="p-2 font-bold bg-red-500 text-white rounded-md ">X</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GuacamoleRedirect',
  data () {
    return {
      token: '',
      showIframe: false
    }
  },
  methods: {
    loadIframe () {
      // Demander le JWT
      fetch('http://192.168.1.1:2616/fireedge/api/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user: process.env.VUE_APP_USERNAME,
          token: process.env.VUE_APP_TOKEN
        })
      })
        .then(response => response.json())
        .then(data => {
          console.log('user:', process.env.VUE_APP_USERNAME)
          console.log('token:', process.env.VUE_APP_TOKEN)
          // Récupérer le token JWT
          this.token = data.data.token
          // Show the iframe
          this.showIframe = true
          // Load the iframe source after showing
          this.$nextTick(() => {
            this.$refs.iframe.src = `http://192.168.1.1:2616/fireedge/sunstone/guacamole/12/vnc?externalToken=${this.token}`
            this.$refs.iframe.focus()
          })
        })
        .catch(error => {
          console.error('Erreur lors de la récupération du JWT :', error)
        })
    },
    closeIframe () {
      // Clear iframe src to stop any ongoing processing
      this.$refs.iframe.src = ''
      this.showIframe = false
    }
  }
}
</script>

<style scoped>
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
