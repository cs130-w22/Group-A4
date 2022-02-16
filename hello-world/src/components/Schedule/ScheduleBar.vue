<template>
  <div>
    <v-btn fixed fab dark @click.stop="drawer = !drawer">
      <v-icon> mdi-pencil </v-icon>
    </v-btn>
    <v-navigation-drawer
      v-model="drawer"
      bottom
      temporary
      width="25vw"
      app
      hide-overlay
      right
    >
      <SchedulePlacesCard></SchedulePlacesCard>
    </v-navigation-drawer>
  </div>
</template>

<script>
import SchedulePlacesCard from "./SchedulePlacesCard.vue";
export default {
  name: "ScheduleBar",
  components: {
    SchedulePlacesCard,
  },
  data: () => ({
    drawer: false,
  }),
};
</script>
<style scoped>
.v-btn {
  top: 120px;
  left: 20px;
  margin: 0 0 16px 16px;
}
</style>