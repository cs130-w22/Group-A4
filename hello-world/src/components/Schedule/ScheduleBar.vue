<template>
  <div>
    <v-btn fixed fab dark @click.stop="btnClicked">
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
      stateless
    >
      <SchedulePlacesCard></SchedulePlacesCard>
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
import SchedulePlacesCard from "./SchedulePlacesCard.vue";
export default {
  name: "ScheduleBar",
  components: {
    SchedulePlacesCard,
  },
  data: () => ({
    drawer: true,
    snackbar: false,
  }),

  methods: {
    btnClicked() {
      const selectedPlaces = this.$children[1].$children[0]._data.selected;
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