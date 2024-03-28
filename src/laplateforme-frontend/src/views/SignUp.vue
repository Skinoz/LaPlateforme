<template>
    <div>
        <div>
            <div class="w-full max-w-xs">
                <form @submit.prevent="submitform" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                    <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
                        Username
                    </label>
                    <input v-model="username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username">
                    </div>
                    <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
                        Password
                    </label>
                    <input v-model="password" class="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="******************">
                    </div>
                    <div class="flex items-center justify-between">
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
                        S'enregistrer
                    </button>
                    </div>
                </form>
                <div v-if="errors.length" role="alert">
                    <div class="border border-t-0 border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700">
                        <p v-for="error in errors" v-bind:key="error">
                            {{ error }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'SignUp',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    methods: {
        submitform(e) {
            const formData = {
                username: this.username,
                password: this.password
            }

            axios
                .post("/api/v1/users/", formData)
                .then(response => {
                    console.log(response)
                    this.$router.push('/log-in')
                })
                .catch(error => {
                    if (error.response) {
                        for (const proprety in error.response.data) {
                            this.errors.push(`${proprety}: ${error.response.data[proprety]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>