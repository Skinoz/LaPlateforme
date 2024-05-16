import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NetworkGraph from '../views/Nebula/NebulaGraph.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'

import store from '../store'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/network',
    name: 'network',
    component: NetworkGraph,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LogIn
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
