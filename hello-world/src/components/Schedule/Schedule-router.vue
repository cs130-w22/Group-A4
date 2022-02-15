<template>
  <v-row>
    <ScheduleBar></ScheduleBar>

    <v-col cols="12" sm="8">
      <v-sheet rounded="lg" min-height="90vh">
        <ScheduleMap> </ScheduleMap>
      </v-sheet>
    </v-col>
    <v-col cols="12" sm="4">
      <v-sheet rounded="lg" min-height="90vh">
        <ScheduleTimeline> </ScheduleTimeline>
      </v-sheet>
    </v-col>
  </v-row>
</template>
<script>
import ScheduleMap from "./ScheduleMap";
import ScheduleBar from "./ScheduleBar.vue";
import ScheduleTimeline from "./ScheduleTimeline.vue";

export default {
  name: "ScheduleRouter",
  components: {
    ScheduleMap,
    ScheduleTimeline,
    ScheduleBar,
  },
};
</script>