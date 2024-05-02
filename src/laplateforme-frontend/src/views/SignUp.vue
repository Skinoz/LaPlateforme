<template>
  <div class="bg-[#121827] h-[calc(100vh-70px)]">
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 ">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm ">
        <img class="mx-auto h-10 w-auto" src="../assets/LP.png" alt="Company">
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-white">S'inscrire à LaPlateforme</h2>
      </div>
      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <div v-if="errors.length" class="bg-red-100 text-left border border-red-400 text-red-700 px-4 py-3 my-4 rounded relative" role="alert">
          <span v-for="error in errors" v-bind:key="error" class="block sm:inline">- {{ error }}<br></span>
          <span class="absolute top-0 bottom-0 right-0 px-4 py-3">
            <button @click="closeError">
              <svg class="fill-current h-6 w-6 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
            </button>
          </span>
        </div>
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label for="username" class="block text-left text-sm font-medium leading-6 text-white">Pseudonyme</label>
            <div class="mt-2">
              <input v-model="username" id="username" name="username" required autocomplete="username" class="block w-full px-2 rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-black focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm font-medium leading-6 text-white">Mot de passe</label>
              <div class="text-sm">
                <a href="#" class="font-semibold text-[#d9caad]">Forgot password?</a>
              </div>
            </div>
            <div class="mt-2">
              <input v-model="password" id="password" name="password" type="password" required autocomplete="current-password" class="block px-2 text-left w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <button type="submit" class="flex w-full justify-center rounded-md bg-[#d9caad] px-3 py-1.5 text-sm font-semibold leading-6 text-[#121827] shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'LogIn',
  data () {
    return {
      username: '',
      password: '',
      errors: []
    }
  },
  methods: {
    submitForm () {
      this.errors = []
      if (this.username === '') {
        this.errors.push('Le champ pseudonyme est obligatoire')
      }
      if (this.password === '') {
        this.errors.push('Le champ mot de passe est obligatoire')
      }
      if (this.errors.length === 0) {
        const formData = {
          username: this.username,
          password: this.password
        }
        axios
          .post(process.env.VUE_APP_PROTOCOL + '://' + process.env.VUE_APP_HOST_BACKEND_SERVER + ':' + process.env.VUE_APP_PORT + '/api/v1/users/', formData)
          .then(response => {
            console.log(response)
            this.$router.push({ name: 'login' })
          })
          .catch(error => {
            console.error('Erreur lors de la connexion :', error)
            this.errors.push('Erreur lors de la connexion')
          })
        console.log(process.env.VUE_APP_PROTOCOL + '://' + process.env.VUE_APP_HOST_BACKEND_SERVER + ':' + process.env.VUE_APP_PORT + '/api/v1/users/')
      }
    },
    closeError () {
      this.errors = []
    }
  }
}

</script>
