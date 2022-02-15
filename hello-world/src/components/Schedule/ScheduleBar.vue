<template>
  <div>
    <v-btn fixed fab dark @click.stop="drawer = !drawer">
      <v-icon> mdi-pencil </v-icon>
    </v-btn>
    <v-navigation-drawer v-model="drawer" bottom temporary width="360" app>
      <v-card>
        <v-card-title>Pick your time</v-card-title>
        <v-card-text>
          <ScheduleTimePicker></ScheduleTimePicker>
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-title>When do you wake up</v-card-title>
        <v-card-text>
          <v-chip-group
            v-model="selection"
            active-class="deep-purple accent-4 white--text"
            column
          >
            <v-chip>5:30AM</v-chip>

            <v-chip>7:30AM</v-chip>

            <v-chip>8:00AM</v-chip>

            <v-chip>9:00AM</v-chip>
          </v-chip-group>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
  </div>
</template>

<script>
import ScheduleTimePicker from "./ScheduleTimePicker.vue";
export default {
  name: "ScheduleBar",
  components: {
    ScheduleTimePicker,
  },
  data: () => ({
    drawer: false,
    selection: 1,
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