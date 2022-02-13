<template>
  <div><Map> </Map> <Timeline> </Timeline></div>
</template>
<script>
import Map from "./Map";
import Timeline from "./Timeline.vue";

export default {
  name: "Schedule",
  components: {
    Map,
    Timeline,
  },
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