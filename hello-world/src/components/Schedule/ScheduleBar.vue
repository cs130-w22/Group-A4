<template>
  <div>
    <v-btn fixed fab dark @click.stop="btnClicked">
      <v-icon> mdi-pencil </v-icon>
    </v-btn>
    <v-navigation-drawer
      v-model="drawer"
      bottom
      temporary
      :width="$vuetify.breakpoint.lgAndUp ? '25vw' : '50vw'"
      app
      hide-overlay
      right
      stateless
    >
      <SchedulePlaceCards ref="placeCards"></SchedulePlaceCards>
    </v-navigation-drawer>
    <v-snackbar
      v-model="snackbar"
      color="red accent-2"
      absolute
      top
      timeout="1000"
    >
      <div class="text-center font-weight-bold">Select at least one place</div>
    </v-snackbar>
  </div>
</template>

<script>
import SchedulePlaceCards from "./SchedulePlaceCards.vue";
export default {
  name: "ScheduleBar",
  components: {
    SchedulePlaceCards,
  },
  data: () => ({
    drawer: true,
    snackbar: false,
  }),

  methods: {
    btnClicked() {
      const selectedPlaces = this.$refs.placeCards.selected;
      if (selectedPlaces.length === 0) {
        this.snackbar = true;
        return;
      }
      this.drawer = !this.drawer;
    },
  },
};
</script>
<style scoped>
.v-btn {
  top: 120px;
  left: 20px;
  margin: 0 0 16px 16px;
}
</style>