import Vue from 'vue'
import App from './App.vue'
import VueGeolocation from 'vue-browser-geolocation'


import GSignInButton from 'vue-google-signin-button'
Vue.use(GSignInButton)

Vue.config.productionTip = false
Vue.use(VueGeolocation)

import * as VueGoogleMaps from 'vue2-google-maps'
import vuetify from './plugins/vuetify'
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCrt7b1kPOg4J7ayO6IgIJfy6R_9vp5Rlw'
  }
})



new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')