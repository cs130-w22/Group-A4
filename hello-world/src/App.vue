<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-tabs centered class="ml-n9" color="grey darken-1">
        <v-tab v-for="link in links" :key="link.name" :to="link.name">
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
          v-if="!isSignIn"
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
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
// import axios from "axios";

import UserPanel from "./components/UserPanel.vue";

export default {
  name: "App",

  components: {
    UserPanel,
  },

  data: () => ({
    links: [{ name: "Map" }, { name: "Schedule" }],
    isSignIn: false,
    isInit: false,
    access_token: null,
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
      // axios
      //   .post("http://localhost:8000/auth/google/", {
      //     access_token: token,
      //   })
      //   .then((resp) => {
      //     this.user = resp.data.user;
      //   })
      //   .catch((err) => {
      //     console.log(err.response);
      //   });

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
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
