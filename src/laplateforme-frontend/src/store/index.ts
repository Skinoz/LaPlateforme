/* ./Store/index.ts défini un store Vuex pour gérer l'état de l'application.
* Il contient un objet d'état avec trois propriétés: user, isAuthenticated et token.
* Il contient également des mutations pour initialiser le store (initializeStore), définir le jeton (setToken) et supprimer le jeton (removeToken).
* Ces mutations sont appelées par des actions pour modifier l'état du store.
* Le store est exporté pour être utilisé dans l'application.
*/

import { createStore, Store } from 'vuex'

// Define the state interface
interface State {
  user: {
    username: string;
  };
  isAuthenticated: boolean;
  token: string;
}

// Create a new store instance.
const store: Store<State> = createStore({
  state: {
    user: {
      username: ''
    },
    isAuthenticated: false,
    token: ''
  },
  getters: {
  },
  mutations: {
    initializeStore (state: State) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token') || ''
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
      console.log(state.isAuthenticated) // état de l'authentification
    },
    setToken (state: State, token: string) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken (state: State) {
      state.token = ''
      state.isAuthenticated = false
    }
  },
  actions: {
  },
  modules: {
  }
})

export default store
