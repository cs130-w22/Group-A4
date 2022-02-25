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
export default {
  name: "ItineraryTabs",

  data() {
    return {
      tab: null,
      itineraryNames: [],

      text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    };
  },

  created() {
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
