<template>
  <v-row>
    <v-col cols="6">
      <v-sheet rounded="lg" min-height="90vh">
        <ItineraryMap></ItineraryMap>
      </v-sheet>
    </v-col>
    <v-col cols="6">
      <ItineraryTabs ref="ItineraryTabs"></ItineraryTabs>
    </v-col>
  </v-row>
</template>
<script>
import ItineraryMap from "./ItineraryMap";
import ItineraryTabs from "./ItineraryTabs";

export default {
  name: "ItineraryRouter",
  components: {
    ItineraryMap,
    ItineraryTabs,
  },
};
</script>