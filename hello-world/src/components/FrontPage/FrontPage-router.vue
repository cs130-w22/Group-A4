<template>
  <v-row>
    <v-col cols="12">
      <FrontPageBackground></FrontPageBackground>
    </v-col>
  </v-row>
</template>

<script>
import FrontPageBackground from "./FrontPageBackground.vue";

export default {
  name: "FrontPageRouter",
  components: {
    FrontPageBackground,
  },
};
</script>

<style>
</style>