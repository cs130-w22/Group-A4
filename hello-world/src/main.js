import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

import VueGeolocation from 'vue-browser-geolocation'
import GAuth from 'vue-google-oauth2'

import * as VueGoogleMaps from 'vue2-google-maps'

const gauthOption = {
  clientId: '113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com',
  scope: 'profile email',
  prompt: 'select_account'
}

Vue.use(GAuth, gauthOption)

Vue.config.productionTip = false

Vue.use(VueGeolocation)
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCrt7b1kPOg4J7ayO6IgIJfy6R_9vp5Rlw',
    libraries: 'places',
  },
  installComponents: true
})


new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')