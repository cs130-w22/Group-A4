<template>
  <v-stepper
    v-model="e6"
    vertical
    non-linear
    min-height="90vh"
    elevation="0"
    rounded="lg"
  >
    <v-stepper-step :complete="e6 > 1" step="1">
      Select an place
      <small>New York City</small>
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-btn color="primary" @click="e6 = 2"> Continue </v-btn>
      <v-btn text> Cancel </v-btn>
    </v-stepper-content>

    <v-stepper-step step="2" editable edit-icon="$complete">
      Select the length of your trip
    </v-stepper-step>

    <v-stepper-content step="2">
      <v-card>
        <v-card-title>Pick your time</v-card-title>
        <v-card-text>
          <ScheduleTimePicker></ScheduleTimePicker>
        </v-card-text>

        <v-divider class="mx-1"></v-divider>

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
        <v-btn color="primary" @click="e6 = 3"> Confirm </v-btn>
      </v-card>
    </v-stepper-content>

    <v-stepper-step :complete="step3" step="3" editable edit-icon="$complete">
      Pick your places of interest
    </v-stepper-step>

    <v-stepper-content step="3">
      <v-btn color="primary" @click="(step3 = true), e6++"> Confirm </v-btn>
    </v-stepper-content>

    <v-stepper-step :complete="e6 > 4" step="4" editable edit-icon="$complete">
      Pick your places of interest
    </v-stepper-step>

    <v-stepper-content step="4">
      <v-btn color="primary" @click="e6 = 5"> Generate itinerary </v-btn>
    </v-stepper-content>

    <!-- <v-stepper-step :complete="e6 > 4" step="4" editable>
      View setup instructions
    </v-stepper-step>
    <v-stepper-content step="4">
      <v-btn color="primary" @click="e6 = 1"> Continue </v-btn>
      <v-btn text> Cancel </v-btn>
    </v-stepper-content> -->
  </v-stepper>
</template>

<script>
import ScheduleTimePicker from "./ScheduleTimePicker.vue";
export default {
  name: "ScheduleStepper",
  components: {
    ScheduleTimePicker,
  },
  data() {
    return {
      e6: 2,
      selection: 1,
      step3: false,
    };
  },
};
</script>

