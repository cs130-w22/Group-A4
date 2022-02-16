<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-tabs centered class="ml-n9" color="grey darken-1">
        <v-tab v-for="link in links" :key="link.name" :to="link.name">
          {{ link.name }}
        </v-tab>
      </v-tabs>

      <g-signin-button
        v-if="isEmpty(user)"
        :params="googleSignInParams"
        @success="onGoogleSignInSuccess"
        @error="onGoogleSignInError"
        style="width: 40px; transform: translateX(-100%)"
      >
        <v-btn dark> Login </v-btn>
      </g-signin-button>
      <user-panel v-else :user="user"></user-panel>
    </v-app-bar>
    <v-main class="grey lighten-2">
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

import UserPanel from "./components/UserPanel.vue";

export default {
  name: "App",

  components: {
    UserPanel,
  },

  data: () => ({
    links: [{ name: "Map" }, { name: "Schedule" }],
    googleSignInParams: {
      client_id:
        "113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com",
    },
    user: {},
  }),

  methods: {
    onGoogleSignInSuccess(resp) {
      const token = resp.wc.access_token;
      axios
        .post("http://localhost:8000/auth/google/", {
          access_token: token,
        })
        .then((resp) => {
          this.user = resp.data.user;
        })
        .catch((err) => {
          console.log(err.response);
        });
    },
    onGoogleSignInError(error) {
      console.log("OH NOES", error);
    },
    isEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
  },
};
</script>
