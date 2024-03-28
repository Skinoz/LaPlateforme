<template>
  <div id="app">
    <nav class="bg-white border-gray-200 dark:bg-gray-900">
      <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <router-link to="/" class="flex items-center space-x-3 rtl:space-x-reverse">
            <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Flowbite Logo" />
            <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">La Plateforme</span>
        </router-link>
        <div class="hidden w-full md:block md:w-auto" id="navbar-default">
          <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <template v-if="$store.state.isAuthenticated">
              <li>
                <router-link to="/dashboard" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500">Dashboard</router-link>
              </li>
            </template>
            <template v-else>
              <li>
                <router-link to="/log-in" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500">Connexion</router-link>
              </li>
              <li>
                <router-link to="/sign-up" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500">S'enregistrer</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    <div class="section">  
      <router-view/>
    </div>
    <footer class="footer">
      <p class="text-center">Copyright (c) 2024</p>
    </footer>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'App',
    beforeCreate() {
      this.$store.commit('initializeStore');
      const token = this.$store.state.token;

      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token" + token
      }else{
        axios.defaults.headers.common['Authorization'] = ""
      }
    },
  }

</script>

<style lang="scss">

</style>
