<template>
  <div>
    Saved trip

    <v-toolbar dense flat>
      <v-tabs v-model="tab" centered center-active show-arrows optional>
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
    </v-toolbar>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in itineraryNames" :key="item">
        <!-- <v-card flat> -->
        <div
          class="text-h6 my-4 text-center"
          v-text="item"
          style="word-break: break-word"
        ></div>

        <ItineraryTimeline> </ItineraryTimeline>
        <!-- <v-card-text v-text="text"></v-card-text> -->
        <!-- </v-card> -->
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import ItineraryTimeline from "./ItineraryTimeline";

export default {
  name: "ItineraryTabs",
  components: {
    ItineraryTimeline,
  },
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
};
</script>
