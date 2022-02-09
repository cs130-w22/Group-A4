<template>
  <!-- <v-app-bar app color="primary" dark> -->
  <!-- <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div> -->

  <!-- <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn> -->

  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-avatar
        :color="$vuetify.breakpoint.smAndDown ? 'grey darken-1' : 'transparent'"
        size="32"
      ></v-avatar>

      <v-tabs centered class="ml-n9" color="grey darken-1">
        <v-tab v-for="link in links" :key="link">
          {{ link }}
        </v-tab>
      </v-tabs>


      <g-signin-button
        v-if="isEmpty(user)"
        :params="googleSignInParams"
        @success="onGoogleSignInSuccess"
        @error="onGoogleSignInError"
      >
        <button class="btn btn-block btn-success">
          Google Signin
        </button>
      </g-signin-button>
      <user-panel v-else :user="user"></user-panel>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col cols="12" sm="2">
            <v-sheet rounded="lg" min-height="268"> <Stepper /> </v-sheet>
          </v-col>

          <v-col cols="12" sm="10">
            <v-sheet min-height="70vh" rounded="lg">
              <Map />
            </v-sheet>
          </v-col>

          <!-- <v-col cols="12" sm="2">
            <v-sheet rounded="lg" min-height="268"> </v-sheet>
          </v-col> -->
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'


import Map from "./components/Map";
import Stepper from "./components/Stepper";
import UserPanel from './components/UserPanel.vue'
// import Form from "./components/Form";

export default {
  name: "App",

  components: {
    Map,
    Stepper,
    UserPanel
  },

  data: () => ({
    links: ["Map", "Profile", "Schedule"],
    googleSignInParams: {
      client_id: '600729137370-h25svjos6nbofm48mmtacd3hjq6ogu95.apps.googleusercontent.com'
    },
    user: {},

  }),

  methods: {
    onGoogleSignInSuccess (resp) {
      console.log(resp)

      const token = resp.wc.access_token
      axios.post('http://localhost:8000/auth/google/', {
        access_token: token
      })
        .then(resp => {
          this.user = resp.data.user
        })
        .catch(err => {
          console.log(err.response)
        })
    },
    onGoogleSignInError (error) {
      console.log('OH NOES', error)
    },
    isEmpty (obj) {
      return Object.keys(obj).length === 0
    }
  }};
</script>
