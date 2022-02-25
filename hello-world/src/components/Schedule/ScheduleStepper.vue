<template>
  <v-stepper
    v-model="e6"
    vertical
    non-linear
    min-height="90vh"
    elevation="0"
    rounded="lg"
  >
    <v-stepper-step complete step="1">
      Select an place
      <small class="font-weight-bold"> {{ location }}</small>
    </v-stepper-step>

    <v-stepper-content step="1">
      <!-- <v-btn color="primary" @click="e6 = 2"> Continue </v-btn> -->
      <!-- <v-btn text> Cancel </v-btn> -->
    </v-stepper-content>

    <v-stepper-step complete step="2">
      Pick your places of interest
      <small class="font-weight-bold"> The battery, nyc stock exchange </small>
    </v-stepper-step>

    <v-stepper-content step="2">
      <!-- <v-btn color="primary" @click="e6 = 3"> Continue </v-btn> -->
    </v-stepper-content>

    <v-stepper-step :complete="step3" step="3" editable edit-icon="$complete">
      Select the length of your trip
    </v-stepper-step>

    <v-stepper-content step="3">
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
        <v-btn color="primary" @click="(step3 = true), e6++"> Confirm </v-btn>
      </v-card>
    </v-stepper-content>

    <v-stepper-step :complete="e6 > 4" step="4" editable edit-icon="$complete">
      Finalize detail
      <small class="font-weight-bold"
        >Some places may not in the final schedule
      </small>
    </v-stepper-step>

    <v-stepper-content step="4">
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="generateItinerary">
        Generate itinerary
      </v-btn>
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
import axios from "axios";

import ScheduleTimePicker from "./ScheduleTimePicker.vue";
export default {
  name: "ScheduleStepper",
  components: {
    ScheduleTimePicker,
  },
  computed: {
    location() {
      return this.$route.params.location;
    },
  },
  data() {
    return {
      e6: 3,
      selection: 1,
      step3: false,

      userOptions: {
        dates: ["2022-02-22", "2022-02-25"],
        wakeUpTime: "07:30",
        places: [""],
      },
    };
  },

  methods: {
    generateItinerary() {
      const places =
        this.$parent.$parent.$children[2].$refs.placeCards.places.slice(15);

      this.userOptions.places = places;

      this.e6 = 5;
      const headers = {
        Authorization:
          "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1NzU3ODk2LCJpYXQiOjE2NDU2NzE0OTYsImp0aSI6ImI1OWZhZDQwZjQwNzQzMmI4MjhlMTc2MmVmNDhiZDk1IiwidXNlcl9pZCI6MX0.IabsdL3Ht3RqOF5QL8OMAC3A_b6kzeXb5BGZJSpH24k",
      };
      axios
        .post("http://localhost:8000/trip/schedule/", this.userOptions, {
          headers,
        })
        .then((resp) => {
          console.log(resp);
          // this.user = resp.data.user;
          // this.$cookies("access_token",resp.data.access_token)
        })
        .catch((err) => {
          console.log(err.response);
        });
    },
  },
};
</script>

