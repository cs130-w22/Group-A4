<template>
  <v-row>
    <v-col :cols="$vuetify.breakpoint.lgAndUp ? 9 : 6">
      <v-sheet rounded="lg" min-height="90vh">
        <ScheduleMap> </ScheduleMap>
      </v-sheet>
    </v-col>
    <v-col :cols="$vuetify.breakpoint.lgAndUp ? 3 : 6">
      <v-sheet rounded="lg" min-height="90vh">
        <ScheduleStepper> </ScheduleStepper>
      </v-sheet>
    </v-col>
    <ScheduleBar ref="ScheduleBar"></ScheduleBar>
  </v-row>
</template>
<script>
import ScheduleMap from "./ScheduleMap";
import ScheduleBar from "./ScheduleBar.vue";
import ScheduleStepper from "./ScheduleStepper.vue";

export default {
  name: "ScheduleRouter",
  components: {
    ScheduleMap,
    ScheduleStepper,
    ScheduleBar,
  },
};
</script>