<template>
  <v-stepper v-model="e6" vertical min-height="90vh" elevation="0" rounded="lg">
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
    </v-stepper-step>

    <v-stepper-content step="2">
      <!-- <v-btn color="primary" @click="e6 = 3"> Continue </v-btn> -->
    </v-stepper-content>

    <v-stepper-step :complete="e6 > 3" step="3" editable edit-icon="$complete">
      Select the length of your trip
      <small class="font-weight-bold"
        >Some places may not in the final schedule
      </small>
    </v-stepper-step>

    <v-stepper-content step="3">
      <v-card>
        <v-card-title>When do you want to travel</v-card-title>
        <v-card-text>
          <v-date-picker
            v-model="dates"
            range
            show-adjacent-months
            width="100%"
            :allowed-dates="allowedDates"
          >
          </v-date-picker>
        </v-card-text>

        <v-divider class="mx-1"></v-divider>

        <v-card-title>When do you want to wake up</v-card-title>
        <v-card-text>
          <v-chip-group
            v-model="selection"
            active-class="deep-purple accent-4 white--text"
            column
          >
            <v-chip v-for="time in wakeUpTime" :key="time">{{ time }}</v-chip>
          </v-chip-group>
        </v-card-text>
        <!-- <v-btn color="primary" @click="(step3 = true), e6++"> Confirm </v-btn> -->
        <v-btn color="primary" @click="generateItinerary">
          Generate itinerary
        </v-btn>
      </v-card>
    </v-stepper-content>
    <!-- 
    <v-stepper-step :complete="e6 > 4" step="4" editable edit-icon="$complete">
      Finalize detail
      <small class="font-weight-bold"
        >Some places may not in the final schedule
      </small>
    </v-stepper-step>

    <v-stepper-content step="4">
      <v-spacer></v-spacer>
    </v-stepper-content> -->

    <v-progress-linear
      reverse
      query
      :indeterminate="loading"
    ></v-progress-linear>

    <v-snackbar
      v-model="snackbar"
      color="red accent-2"
      absolute
      top
      timeout="1000"
    >
      <div class="text-center font-weight-bold">
        Select 2 dates for your trip
      </div>
    </v-snackbar>
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

export default {
  name: "ScheduleStepper",

  computed: {
    location() {
      return this.$route.params.location;
    },
    userOptions() {
      return {
        dates: this.dates,
        wakeUpTime: this.wakeUpTime[this.selection].substring(0, 5),
        places: [],
      };
    },
  },
  data() {
    return {
      e6: 3,
      selection: 1,
      loading: false,
      snackbar: false,
      dates: [],
      wakeUpTime: ["07:30AM", "08:00AM", "08:30AM", "09:00AM"],
    };
  },

  methods: {
    allowedDates(val) {
      const today = new Date();
      const candidateDay = new Date(val);
      return today <= candidateDay;
    },
    generateItinerary() {
      if (this.dates.length < 2) {
        this.snackbar = true;
        return;
      }

      const places =
        this.$parent.$parent.$children[2].$refs.placeCards.places.slice(15);

      this.userOptions.places = places;

      this.e6 = 5;

      const ac_token = this.$cookie.get("access_token");
      if (ac_token !== null) {
        const headers = {
          "Content-Type": "application/json",
          Authorization: "Bearer " + ac_token,
        };

        this.loading = true;
        axios
          .post("http://localhost:8000/trip/schedule/", this.userOptions, {
            headers,
          })
          .then((resp) => {
            this.loading = false;
            this.$router.push({
              path: "/itinerary/" + resp.data.id,
              params: { new_itinerary: true },
            });
            // console.log(resp);
          })
          .catch((err) => {
            this.loading = false;
            console.error(err);
          });
      } else {
        console.log("User does not have access token");
      }
    },
  },
};
</script>

