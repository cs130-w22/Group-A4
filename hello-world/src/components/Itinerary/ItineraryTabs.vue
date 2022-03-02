<template>
  <v-sheet rounded="lg" height="90vh">
    <v-overlay :value="overlay" absolute>
      <v-btn
        v-if="isInit"
        class="white--text"
        color="teal"
        v-on:click="onSignInClicked"
      >
        Log in to see this page
      </v-btn>
    </v-overlay>
    <v-tabs
      dark
      background-color="teal darken-3"
      v-model="tab"
      center-active
      show-arrows
      @change="onTabChanged"
      hide-slider
      optional
      class="ItineraryTabs"
    >
      <v-tab v-for="(itinerary, index) in itinerarys" :key="itinerary.id">
        <v-badge v-if="index === 0" color="pink" dot>
          <span>{{ itinerary.title }} </span>
        </v-badge>
        <span v-else>
          {{ itinerary.title }}
        </span>
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="itinerary in itinerarys" :key="itinerary.id">
        <router-view v-if="itinerary.id === activeTabId"></router-view>
      </v-tab-item>
    </v-tabs-items>
  </v-sheet>
</template>

<script>
import axios from "axios";

export default {
  name: "ItineraryTabs",

  data() {
    return {
      tab: -1,
      itinerarys: [],
      overlay: true,
    };
  },

  computed: {
    isSignIn() {
      return this.$root.$children[0].isSignIn;
    },

    isInit() {
      return this.$root.$children[0].isInit;
    },

    activeTabId() {
      if (this.tab === undefined || this.tab === -1) return null;

      return this.itinerarys[this.tab].id;
    },
  },
  watch: {
    isSignIn: {
      immediate: true,
      deep: true,
      handler() {
        if (!this.isInit) return;
        if (this.isSignIn) {
          const access_token = this.$cookie.get("access_token");

          const headers = {
            "Content-Type": "application/json",
            Authorization: "Bearer " + access_token,
          };

          axios
            .get("http://127.0.0.1:8000/trip/itinerary/", {
              headers,
            })
            .then((resp) => {
              this.itinerarys = resp.data;
              this.overlay = false;
            })
            .catch((err) => {
              console.error(err);
            });
        } else {
          this.itinerarys = [];
          this.overlay = true;
          this.tab = -1;
          if (this.$route.path !== "/itinerary") {
            // prevent double navigation
            this.$router.push({ path: "/itinerary", replace: true });
          }
        }
      },
    },
  },

  methods: {
    onSignInClicked() {
      this.$root.$children[0].onSignInClicked();
    },
    onTabChanged() {
      if (this.tab === undefined) {
        this.$router.push("/itinerary");
      } else {
        this.$router.push("/itinerary/" + this.activeTabId);
      }
    },
  },
};
</script>

<style scoped>
.v-tab--active {
  color: rgba(255, 255, 255, 0.6);
}
</style>
