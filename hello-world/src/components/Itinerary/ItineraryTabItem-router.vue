<template>
  <div>
    <!-- <ItineraryMap></ItineraryMap> -->

    <ItineraryTimeline v-if="timeline !== null" :timeline="timeline">
    </ItineraryTimeline>
  </div>
</template>

<script>
import ItineraryTimeline from "./ItineraryTimeline";
// import ItineraryMap from "./ItineraryMap";

import axios from "axios";

export default {
  name: "ItineraryTabItemRouter",
  props: ["id"],
  components: {
    ItineraryTimeline,
    // ItineraryMap,
  },

  data() {
    return {
      timeline: null,
    };
  },
  created() {
    const ac_token = this.$cookie.get("access_token");

    if (ac_token !== null) {
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + ac_token,
      };

      axios
        .get("http://127.0.0.1:8000/trip/itinerary/" + this.id, {
          headers,
        })
        .then((resp) => {
          this.timeline = resp.data;
        })
        .catch((err) => {
          console.error(err);
        });
    } else {
      console.log("User does not have access token");
    }
  },
};
</script>