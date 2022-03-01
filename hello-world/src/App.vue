<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-tabs centered class="ml-n9" color="grey darken-1">
        <v-tab v-for="link in links" :key="link.route" :to="link.route">
          {{ link.name }}
        </v-tab>
      </v-tabs>

      <div style="width: 48px">
        <v-btn
          v-if="!user"
          dark
          @click="onSignInClicked"
          style="transform: translateX(-50%)"
          :style="{ display: isInit ? '' : 'none' }"
        >
          Login
        </v-btn>
        <user-panel
          :user="user"
          v-else
          v-on:sign-out="onSignOutClicked"
          :style="{ display: isInit ? '' : 'none' }"
        ></user-panel>
      </div>
    </v-app-bar>
    <v-main class="grey lighten-2">
      <v-container fluid>
        <keep-alive>
          <router-view> </router-view>
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
    user: null,
  }),
  created() {
    const checkGauthLoad = setInterval(() => {
      this.isInit = this.$gAuth.isInit;
      this.isSignIn = this.$gAuth.isAuthorized;
      if (this.isInit) clearInterval(checkGauthLoad);
    }, 1000);

    const ac_token = this.$cookie.get("access_token");
    if (ac_token) {
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + ac_token,
      };
      axios
        .get("http://localhost:8000/user/profile/", {
          headers,
        })
        .then((resp) => {
          this.user = resp.data;
        })
        .catch((err) => console.error(err));
    }
  },
  methods: {
    onSignInClicked() {
      this.$gAuth
        .signIn() // log in from the frontend
        .then((googleUser) => {
          if (!googleUser) return;
          // console.log("getAuthResponse", googleUser.getAuthResponse());
          // console.log(
          // "getAuthResponse",
          // this.$gAuth.GoogleAuth.currentUser.get().getAuthResponse()
          // );

          // log in from the backend
          axios
            .post("http://localhost:8000/auth/google/", {
              access_token: googleUser.getAuthResponse().access_token,
            })
            .then((resp) => {
              this.$cookie.set("access_token", resp.data.access_token, {
                expires: "1D",
              });
              this.user = resp.data.user;
              this.isSignIn = this.$gAuth.isAuthorized;
            });
        })
        .catch((err) => {
          console.error(err);
        });
    },

    onSignOutClicked() {
      // log out from the frontend
      this.$gAuth
        .signOut()
        .then(() => {
          // log out from the backend
          axios.post("http://localhost:8000/logout/").then(() => {
            this.$cookie.delete("access_token");
            this.user = null;
            this.isSignIn = this.$gAuth.isAuthorized;
          });
        })
        .catch((err) => {
          console.error(err);
        });

      // this.$router.push("/home");
    },
  },
};
</script>
