<template>
  <v-row>
    <!-- <v-col cols="12" sm="2">
      <v-sheet rounded="lg" min-height="90vh">
        <FrontPageStepper> </FrontPageStepper>
      </v-sheet>
    </v-col> -->
    <v-col cols="12" sm="12">
      <v-sheet rounded="lg" min-height="90vh">
        <FrontPageMap> </FrontPageMap>
        <FrontPageSlideShow> </FrontPageSlideShow>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import FrontPageMap from "./FrontPageMap.vue";
import FrontPageSlideShow from "./FrontPageSlideShow.vue";

export default {
  name: "FrontPageRouter",
  components: {
    FrontPageMap,
    FrontPageSlideShow,
  },
};
</script>

<style>
</style>