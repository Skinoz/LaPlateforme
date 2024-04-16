import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VNetworkGraph from 'v-network-graph'

import './assets/css/tailwind.css'
import 'v-network-graph/lib/style.css'

import store from './store'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(VNetworkGraph)
app.mount('#app')
