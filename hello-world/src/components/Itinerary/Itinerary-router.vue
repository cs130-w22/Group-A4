<template>
  <v-row>
    <v-col cols="12" sm="9">
      <v-sheet rounded="lg" min-height="90vh">
        <ItineraryMap></ItineraryMap>
      </v-sheet>
    </v-col>
    <v-col cols="12" sm="3">
      <v-sheet rounded="lg" min-height="90vh">
        <ItineraryTabs></ItineraryTabs>
      </v-sheet>
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