<template>
  <v-row>
    <ScheduleBar></ScheduleBar>

    <v-col cols="12" sm="9">
      <v-sheet rounded="lg" min-height="90vh">
        <ScheduleMap> </ScheduleMap>
      </v-sheet>
    </v-col>
    <v-col cols="12" sm="3">
      <v-sheet rounded="lg" min-height="90vh">
        <ScheduleStepper> </ScheduleStepper>
      </v-sheet>
    </v-col>
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