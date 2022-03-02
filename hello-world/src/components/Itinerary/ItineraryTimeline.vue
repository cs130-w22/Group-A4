<template>
  <v-card
    class="mx-auto overflow-y-auto"
    :height="$vuetify.breakpoint.lgAndUp ? '85vh' : '80vh'"
  >
    <v-card-title class="text-h5 ml-10">
      {{ timeline.title }}
    </v-card-title>

    <div
      v-for="[day_date, day_event] of Object.entries(timeline.trip_event)"
      :key="day_event.id"
    >
      <v-container class="fill-height">
        <v-row align="center">
          <strong
            class="display-1 font-weight-regular mr-4"
            style="margin-left: 54px"
            >{{ convertToDate(day_date).getUTCDate() }}</strong
          >
          <v-col justify="end">
            <div class="title font-weight-light">
              {{ dayInWeeks[convertToDate(day_date).getUTCDay()] }}
            </div>
            <div class="text-uppercase font-weight-light">
              {{ monthInYears[convertToDate(day_date).getUTCMonth()] }}
              {{ convertToDate(day_date).getUTCFullYear() }}
            </div>
          </v-col>
        </v-row>
      </v-container>
      <v-card-text class="py-0">
        <v-timeline align-top dense>
          <div v-for="(place, index) in day_event" :key="place.id">
            <v-timeline-item
              :color="index % 2 === 1 ? 'pink' : 'teal lighten-3'"
              small
            >
              <v-row class="pt-1">
                <v-col cols="4">
                  <strong>
                    {{ convertToDate(place.start_time).getUTCHours() }} : 00 -
                    {{ convertToDate(place.end_time).getUTCHours() }} : 00
                  </strong>
                </v-col>
                <v-col cols="8">
                  <strong>{{ place.place_name }}</strong>
                  <v-icon
                    color="primary"
                    class="ml-1"
                    @click="showPlace(place)"
                  >
                    mdi-information
                  </v-icon>
                </v-col>
              </v-row>
            </v-timeline-item>
          </div>
        </v-timeline>
      </v-card-text>
    </div>
  </v-card>
</template>
<script>
export default {
  name: "ItineraryTimeline",
  props: ["timeline"],
  data() {
    return {
      dayInWeeks: [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ],
      monthInYears: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ],
    };
  },
  methods: {
    convertToDate(date_str) {
      return new Date(date_str);
    },
    showPlace(place) {
      this.$root.$emit("show-place-on-itinerary-map", place);
    },

    addMarker(place) {
      this.$root.$emit("add-marker-on-itinerary-map", place);
    },
  },
  created() {
    // this.timeline.trip_event
    for (const day_event of Object.values(this.timeline.trip_event)) {
      day_event.forEach((place) => this.addMarker(place));
    }
  },
};
</script>