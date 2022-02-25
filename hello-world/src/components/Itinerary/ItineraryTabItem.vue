<template>
  <div>
    {{ id }}

    <ItineraryTimeline> </ItineraryTimeline>
  </div>
</template>

<script>
import ItineraryTimeline from "./ItineraryTimeline";

export default {
  name: "ItineraryTabItem",
  props: ["id"],
  components: {
    ItineraryTimeline,
  },
};
</script>