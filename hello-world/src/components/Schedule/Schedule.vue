<template>
  <v-container fluid>
    <v-row>
      <ScheduleBar></ScheduleBar>
      <v-col cols="12" sm="8">
        <Map> </Map>
      </v-col>
      <v-col cols="12" sm="4">
        <ScheduleTimeline> </ScheduleTimeline>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import Map from "../Map";
import ScheduleBar from "./ScheduleBar.vue";
import ScheduleTimeline from "./ScheduleTimeline.vue";

export default {
  name: "Schedule",
  components: {
    Map,
    ScheduleTimeline,
    ScheduleBar,
  },
};
</script>