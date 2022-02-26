<template>
  <v-sheet rounded="lg" height="90vh">
    <v-card color="teal darken-3">
      <v-card-title class="text-center justify-center py-3">
        <h1 class="white--text font-weight-bold text-h2">Saved trip</h1>
      </v-card-title>
    </v-card>
    <v-divider></v-divider>
    <v-divider></v-divider>
    <v-divider></v-divider>

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
      <v-tab v-for="(item, index) in itineraryNames" :key="item">
        <v-badge v-if="index === 0" color="pink" dot>
          <span>
            {{ item.length > 8 ? item.substring(0, 8) + ".." : item }}
          </span>
        </v-badge>
        <span v-else>
          {{ item.length > 8 ? item.substring(0, 8) + ".." : item }}
        </span>
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in itineraryNames" :key="item">
        <router-view v-if="item === itineraryNames[tab]"></router-view>
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
      tab: null,
      itineraryNames: [],
    };
  },

  created() {
    const headers = {
      "Content-Type": "application/json",
      Authorization:
        "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1NzU3ODk2LCJpYXQiOjE2NDU2NzE0OTYsImp0aSI6ImI1OWZhZDQwZjQwNzQzMmI4MjhlMTc2MmVmNDhiZDk1IiwidXNlcl9pZCI6MX0.IabsdL3Ht3RqOF5QL8OMAC3A_b6kzeXb5BGZJSpH24k",
    };

    axios
      .get("http://127.0.0.1:8000/trip/itinerary/", {
        headers,
      })
      .then((resp) => {
        console.log(resp);
        // this.user = resp.data.user;
        // this.$cookies("access_token",resp.data.access_token)
      })
      .catch((err) => {
        console.error(err);
      });

    setTimeout(() => {
      this.itineraryNames = [
        "my trip to nyc",
        "shopping11111111111111111111111111",
        "videos",
        "images",
        "news",
      ];
    }, 1000);
  },

  methods: {
    onTabChanged() {
      if (this.tab === undefined) {
        this.$router.push("/itinerary");
      } else {
        this.$router.push("/itinerary/" + this.itineraryNames[this.tab]);
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
