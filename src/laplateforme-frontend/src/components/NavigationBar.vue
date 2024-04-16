<template>
  <header class="bg-[#051A26] flex justify-between navbar-height px-7">
    <div class="flex items-center justify-center">
      <!-- Add "scoped" attribute to limit CSS to this component only -->
      <img class="h-10" src="../assets/LP.png" alt="Workcation">
    </div>
    <div :class="isOpen ? 'hidden' : 'block'" class="px-2 pt-2 pb-4 hidden sm:flex sm:p-0 items-center justify-center">
      <router-link v-if="store.state.isAuthenticated" to="/network" class="block px-5 py-1 font-semibold rounded text-[#d9caad] text-lg bold ">Graphique du réseau</router-link>
      <router-link to="/" class="block px-5 py-1 font-semibold rounded text-[#d9caad] text-lg bold ">Home</router-link>
    </div>
    <div :class="isOpen ? 'hidden' : 'block'" class="px-2 pt-2 pb-4 hidden sm:flex sm:p-0 items-center">
      <a href="#" class="block px-2 py-1 font-semibold rounded text-[#d9caad] text-lg bold">Login</a>
    </div>
    <div class="sm:hidden">
      <button @click="isOpen = !isOpen" type="button" class="block text-gray-500 hover:text-white focus:text-white focus:outline-none">
        <svg class="h-10 w-8 fill-[#d9caad]" viewBox="0 0 24 24">
          <path v-if="isOpen" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
          <path v-if="!isOpen" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
        </svg>
      </button>
    </div>
  </header>
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
</template>

<script lang="ts">
import { useStore } from 'vuex'
import axios from 'axios'

export default {
  name: 'NavigationBar',
  setup () {
    const store = useStore()

    store.commit('initializeStore')
    const token = store.state.token
    axios.defaults.headers.common.Authorization = token ? `Token ${token}` : ''

    return {
      isOpen: false,
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
