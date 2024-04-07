<template>
  <div id="app" class="">
    <NavigationBar/>
  </div>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/network">Graph</router-link>
  </nav>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import NavigationBar from '@/components/NavigationBar.vue'

@Options({
  components: {
    NavigationBar
  }
})
export default class HomeView extends Vue {}
</script>
