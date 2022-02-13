<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-tabs centered class="ml-n9" color="grey darken-1">
        <v-tab
          v-for="(link, index) in links"
          :key="link.name"
          @change="onTabChange(index)"
        >
          {{ link.name }}
        </v-tab>
      </v-tabs>

      <v-avatar size="60" color="grey darken-3">
        <v-btn v-if="isEmpty(user)" dark>
          <g-signin-button
            :params="googleSignInParams"
            @success="onGoogleSignInSuccess"
            @error="onGoogleSignInError"
          >
            Sign in
          </g-signin-button>
        </v-btn>
        <user-panel v-else :user="user"></user-panel>
      </v-avatar>
    </v-app-bar>
    <v-main class="grey lighten-3">
      <v-container fluid>
        <v-row>
          <v-col v-if="activeTabIndex == 0" cols="12" sm="2">
            <v-sheet rounded="lg" min-height="90vh">
              <Stepper> </Stepper>
            </v-sheet>
          </v-col>
          <!-- <v-col v-else min-height="90vh" cols="12" sm="2">
            <v-sheet rounded="lg" min-height="90vh"> placeHolder </v-sheet>
          </v-col> -->

          <v-col cols="12" :sm="activeTabIndex == 0 ? 10 : 12">
            <v-sheet rounded="lg" min-height="90vh">
              <Map v-if="activeTabIndex == 0"> </Map>
              <SlideShow v-if="activeTabIndex == 0"> </SlideShow>
              <Schedule v-if="activeTabIndex == 1"> </Schedule>
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
import axios from "axios";

import Map from "./components/Map";
import Stepper from "./components/Stepper";
import UserPanel from "./components/UserPanel.vue";
import SlideShow from "./components/SlideShow.vue";
import Schedule from "./components/Schedule/Schedule.vue";

// import Form from "./components/Form";

export default {
  name: "App",

  components: {
    Map,
    Stepper,
    UserPanel,
    SlideShow,
    Schedule,
  },

  data: () => ({
    links: [{ name: "Map" }, { name: "Schedule" }],
    googleSignInParams: {
      client_id:
        "113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com",
    },
    user: {},
    activeTabIndex: 0,
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
    onTabChange(tabToChange) {
      this.activeTabIndex = tabToChange;
    },
  },
};
</script>
