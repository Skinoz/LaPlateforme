<template>
  <header class="bg-[#051A26] flex justify-between navbar-height px-7 z-100 relative">
    <div class="flex items-center justify-center">
      <!-- Add "scoped" attribute to limit CSS to this component only -->
      <img class="h-10" src="../assets/LP.png" alt="Workcation">
    </div>
    <div :class="isOpen ? 'hidden' : 'block'" class="px-2 pt-2 pb-4 hidden sm:flex sm:p-0 items-center justify-center">
      <router-link v-if="store.state.isAuthenticated" to="/network" class="block px-5 py-1 font-semibold rounded text-[#d9caad] text-lg bold ">Graphique du réseau</router-link>
      <router-link to="/" class="block px-5 py-1 font-semibold rounded text-[#d9caad] text-lg bold ">Home</router-link>
    </div>
    <div v-if="!store.state.isAuthenticated" :class="isOpen ? 'hidden' : 'block'" class="px-2 pt-2 pb-4 hidden sm:flex sm:p-0 items-center">
      <router-link to="login" class="block px-2 py-1 font-semibold rounded text-[#d9caad] text-lg bold">Connexion</router-link>
      <router-link to="signup" class="block px-2 py-1 font-semibold rounded text-[#d9caad] text-lg bold">Inscription</router-link>
    </div>
    <div v-if="store.state.isAuthenticated" class="px-2 pt-2 pb-4 hidden sm:flex sm:p-0 items-center">
      <button @click="logout" class="block px-2 py-1 font-semibold rounded text-[#d9caad] text-lg bold">Déconnexion</button>
    </div>
    <div class="sm:hidden">
      <button @click="isOpen = !isOpen" type="button" class="block text-gray-500 hover:text-white focus:text-white focus:outline-none">
        <svg class="h-10 w-8 fill-[#d9caad]" viewBox="0 0 24 24">
          <path v-if="isOpen" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
          <path v-if="!isOpen" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
        </svg>
      </button>
    </div>
    <div  :class="isOpen ? 'block' : 'hidden'" class="px-2 pt-2 pb-4 sm:p-0 sm:hidden bg-[#051A26] rounded-xl mt-5 mx-2 grid grid-cols-3 divide-x-2">
      <!-- Partie Gauche Phone Bar -->
      <div class="grid grid-cols-1 col-span-2 text-left divide-y-2 items-center">
        <div class="text-center rounded">
          <router-link to="/network" class="block px-2 py-2 font-semibold rounded text-[#d9caad] text-lg bold ">Graphique du réseau</router-link>
        </div>
        <div class="text-center rounded">
          <router-link to="/" class="block px-2 py-2 font-semibold rounded text-[#d9caad] text-lg bold ">Home</router-link>
        </div>
      </div>
      <!-- Partie droite Phone Bar -->
      <div>
        <div class=" text-center rounded m-3">
          <a href="#" class="block px-2 py-2 font-semibold rounded text-[#d9caad] text-lg bold ">Connexion</a>
        </div>
        <div class=" text-center rounded m-3">
            <a href="#" class="block px-2 py-2  font-semibold rounded text-[#d9caad] text-lg bold ">S'enregistrer</a>
        </div>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

export default {
  name: 'NavigationBar',
  setup () {
    const store = useStore()
    const router = useRouter()

    store.commit('initializeStore')
    const token = store.state.token

    // Définir le token par défaut pour toutes les requêtes axios
    axios.defaults.headers.common.Authorization = token ? `Token ${token}` : ''

    // Interceptor pour ajouter le token à chaque requête axios
    axios.interceptors.request.use((config) => {
      const token = store.state.token
      if (token) {
        config.headers.Authorization = `Token ${token}`
      }
      return config
    }, (error) => {
      return Promise.reject(error)
    })

    const logout = () => {
      const token = localStorage.getItem('token')
      // API call to logout with djoser endpoint
      axios
        .post(process.env.VUE_APP_PROTOCOL + '://' + process.env.VUE_APP_HOST_BACKEND_SERVER + ':' + process.env.VUE_APP_PORT + '/api/v1/token/logout/')
        .then(response => {
          axios.defaults.headers.common.Authorization = ''
          localStorage.removeItem('token')
          store.commit('removeToken')
          router.push({ name: 'home' })
        })
      console.log(token)
    }

    return {
      isOpen: false,
      logout,
      store
    }
  }
}
</script>

<style>
.navbar-height{
 height: 70px
}
</style>

<!-- Add "scoped" attribute to limit CSS to this component only
<div class="px-4 py-3 sm:p-0">
  <div>
    <img class="h-8" src="../assets/LP.png" alt="Workcation">
  </div>
  <div class="sm:hidden">
    <button @click="isOpen = !isOpen" type="button" class="block text-gray-500 hover:text-white focus:text-white focus:outline-none">
      <svg class="h-6 w-6 fill-current" viewBox="0 0 24 24">
        <path v-if="isOpen" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
        <path v-if="!isOpen" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
      </svg>
    </button>
  </div>
</div>
<nav :class="isOpen ? 'block' : 'hidden'" class="px-2 pt-2 pb-4 sm:flex sm:p-0">
  <a href="#" class="block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800">List your property</a>
  <a href="#" class="mt-1 block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800 sm:mt-0 sm:ml-2">Trips</a>
  <a href="#" class="mt-1 block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800 sm:mt-0 sm:ml-2">Messages</a>
</nav>
<div>
  <a href="#" class="block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800">Login</a>
</div>
-->
