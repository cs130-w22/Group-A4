<template>
  <v-timeline dense clipped class="mr-8">
    <!-- <v-timeline-item fill-dot class="white--text mb-12" color="orange" large>
        <v-text-field
          v-model="input"
          hide-details
          flat
          label="Leave a comment..."
          solo
          @keydown.enter="comment"
        >
          <template v-slot:append>
            <v-btn class="mx-0" depressed @click="comment"> Post </v-btn>
          </template>
        </v-text-field>
      </v-timeline-item> -->

    <v-slide-x-transition group>
      <v-timeline-item
        v-for="event in timeline"
        :key="event.id"
        class="mb-4"
        color="pink"
        small
      >
        <v-row justify="space-between">
          <v-col cols="7" v-text="event.text"></v-col>
          <v-col class="text-right" cols="5" v-text="event.time"></v-col>
        </v-row>
      </v-timeline-item>
    </v-slide-x-transition>

    <v-timeline-item class="mb-6" hide-dot>
      <span>2/11/2022</span>
    </v-timeline-item>

    <v-timeline-item
      class="mb-4"
      color="grey"
      icon-color="grey lighten-2"
      small
    >
      <v-row justify="space-between">
        <v-col cols="7"> Depart from Hotel </v-col>
        <v-col class="text-right" cols="5"> 9:00 EDT </v-col>
      </v-row>
    </v-timeline-item>

    <v-timeline-item class="mb-4" small>
      <v-row justify="space-between">
        <v-col cols="7">
          <v-chip class="white--text ml-0" color="purple" label small>
            Stop 1
          </v-chip>
          Hollywood Sign
        </v-col>
        <v-col class="text-right" cols="5"> 10:00 EDT </v-col>
      </v-row>
    </v-timeline-item>
    <!-- 
      <v-timeline-item class="mb-4" color="grey" small>
        <v-row justify="space-between">
          <v-col cols="7">
            Order confirmation email was sent to John Leider
            (john@vuetifyjs.com).
          </v-col>
          <v-col class="text-right" cols="5"> 15:25 EDT </v-col>
        </v-row>
      </v-timeline-item> -->

    <!-- <v-timeline-item class="mb-4" hide-dot>
        <v-btn class="mx-0"> Resend Email </v-btn>
      </v-timeline-item>

      <v-timeline-item class="mb-4" color="grey" small>
        <v-row justify="space-between">
          <v-col cols="7">
            A $15.00 USD payment was processed on PayPal Express Checkout
          </v-col>
          <v-col class="text-right" cols="5"> 15:25 EDT </v-col>
        </v-row>
      </v-timeline-item> -->

    <v-timeline-item class="mb-4" small>
      <v-row justify="space-between">
        <v-col cols="7">
          <v-chip class="white--text ml-0" color="purple" label small>
            Stop 2
          </v-chip>
          University of California, Los Angeles
        </v-col>
        <v-col class="text-right" cols="5"> 15:25 EDT </v-col>
      </v-row>
    </v-timeline-item>

    <v-timeline-item color="grey" small>
      <v-row justify="space-between">
        <v-col cols="7"> Go back to hotel </v-col>
        <v-col class="text-right" cols="5"> 19:00 EDT </v-col>
      </v-row>
    </v-timeline-item>
  </v-timeline>
</template>
<script>
export default {
  name: "ScheduleTimeline",
  data: () => ({
    events: [],
    input: null,
    nonce: 0,
  }),

  computed: {
    timeline() {
      return this.events.slice().reverse();
    },
  },

  methods: {
    comment() {
      const time = new Date().toTimeString();
      this.events.push({
        id: this.nonce++,
        text: this.input,
        time: time.replace(/:\d{2}\sGMT-\d{4}\s\((.*)\)/, (match, contents) => {
          return ` ${contents
            .split(" ")
            .map((v) => v.charAt(0))
            .join("")}`;
        }),
      });

      this.input = null;
    },
  },
};
</script>