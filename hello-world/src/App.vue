<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-tabs centered class="ml-n9" color="grey darken-1">
        <v-tab v-for="link in links" :key="link.route" :to="link.route">
          {{ link.name }}
        </v-tab>
      </v-tabs>

      <!-- <g-signin-button
        v-if="isEmpty(user)"
        :params="googleSignInParams"
        @success="onGoogleSignInSuccess"
        @error="onGoogleSignInError"
        style="width: 40px; transform: translateX(-100%)"
        </g-signin-button> 
      > -->
      <div style="width: 48px">
        <v-btn
          v-if="!user"
          dark
          @click="handleClickSignIn"
          style="transform: translateX(-50%)"
          :style="{ display: isInit ? '' : 'none' }"
        >
          Login
        </v-btn>
        <user-panel
          :user="user"
          v-else
          v-on:sign-out="handleClickSignOut"
          :style="{ display: isInit ? '' : 'none' }"
        ></user-panel>
      </div>
    </v-app-bar>
    <v-main class="grey lighten-2">
      <v-container fluid>
        <keep-alive>
          <router-view />
        </keep-alive>
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
    links: [
      { name: "New trip", route: "/home" },
      { name: "schedule", route: "/schedule" },
      { name: "itinerary", route: "/itinerary" },
    ],
    isSignIn: false,
    isInit: false,
    access_token: null,
    user: null,
  }),
  created() {
    let that = this;
    let checkGauthLoad = setInterval(function () {
      that.isInit = that.$gAuth.isInit;
      that.isSignIn = that.$gAuth.isAuthorized;
      if (that.isInit) clearInterval(checkGauthLoad);
    }, 1000);
  },
  methods: {
    async handleClickSignIn() {
      try {
        const googleUser = await this.$gAuth.signIn();
        if (!googleUser) return;
        console.log("googleUser", googleUser);
        console.log("getId", googleUser.getId());
        console.log("getBasicProfile", googleUser.getBasicProfile());
        console.log("getAuthResponse", googleUser.getAuthResponse());
        console.log(
          "getAuthResponse",
          this.$gAuth.GoogleAuth.currentUser.get().getAuthResponse()
        );
        this.isSignIn = this.$gAuth.isAuthorized;

        axios
          .post("http://localhost:8000/auth/google/", {
            access_token: googleUser.getAuthResponse().access_token,
          })
          .then((resp) => {
            console.log(resp);
            this.user = resp.data.user;
            // this.$cookies("access_token",resp.data.access_token)
          })
          .catch((err) => {
            console.log(err.response);
          });
      } catch (error) {
        //on fail do something
        console.error(error);
      }
    },

    async handleClickSignOut() {
      try {
        await this.$gAuth.signOut();
        this.isSignIn = this.$gAuth.isAuthorized;
        console.log("isSignIn", this.$gAuth.isAuthorized);

        this.user = null;
      } catch (error) {
        console.error(error);
      }

      // axios
      //   .post("http://localhost:8000/auth/logout/", {
      //     access_token: googleUser.getAuthResponse(),
      //   })
      //   .then((resp) => {
      //     this.delete_cookies(access_token)
      //   })
      //   .catch((err) => {
      //     console.log(err.response);
      //   });
    },
  },
};
</script>
