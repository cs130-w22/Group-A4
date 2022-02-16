import Vue from 'vue'
import App from './App.vue'
import router from './router'

import VueGeolocation from 'vue-browser-geolocation'
import GSignInButton from 'vue-google-signin-button'
import vuetify from './plugins/vuetify'
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false

Vue.use(VueGeolocation)
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCrt7b1kPOg4J7ayO6IgIJfy6R_9vp5Rlw',
    libraries: 'places',
  },
  installComponents: true
})

Vue.use(GSignInButton)


new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')