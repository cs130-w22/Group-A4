import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

import VueGeolocation from 'vue-browser-geolocation'
import GAuth from 'vue-google-oauth2'

import * as VueGoogleMaps from 'vue2-google-maps'

import VueCookie from 'vue-cookie';


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

Vue.use(VueCookie);

import VuetifyGoogleAutocomplete from 'vuetify-google-autocomplete';

Vue.use(VuetifyGoogleAutocomplete, {
  apiKey: 'AIzaSyCrt7b1kPOg4J7ayO6IgIJfy6R_9vp5Rlw', // Can also be an object. E.g, for Google Maps Premium API, pass `{ client: <YOUR-CLIENT-ID> }`
  installComponents: true, // Optional (default: true) - false, if you want to locally install components
  vueGoogleMapsCompatibility: false, // Optional (default: false) - true, requires vue2-google-maps to be configured see https://github.com/xkjyeah/vue-google-maps
});

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')