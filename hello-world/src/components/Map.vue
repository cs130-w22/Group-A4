<template>
  <div>
    <div
      style="
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
      "
    >
      <div>
        <h2>Your coordinates:</h2>
        <p>
          {{ userCoordinates.lat }} Latitude,
          {{ userCoordinates.lng }} Longtitude
        </p>
      </div>

      <div>
        <h2>Map coordinates:</h2>
        <p>
          {{ mapCoordinates.lat }} Latitude, {{ mapCoordinates.lng }} Longtitude
        </p>
      </div>
    </div>

    <GmapMap
      :center="userCoordinates"
      :zoom="zoom"
      style="width: 80%; height: 400px; margin: 32px auto"
      ref="mapRef"
    >
    </GmapMap>
  </div>
</template>

<script>
export default {
  name: "GoogleMap",
  data() {
    return {
      map: null,
      userCoordinates: {
        lat: 0,
        lng: 0,
      },
      zoom: 8,
    };
  },

  created() {
    this.$getLocation({})
      .then((coordinates) => {
        this.userCoordinates = coordinates;
      })
      .catch((error) => alert(error)); // users do not grant permission of the location
  },

  mounted() {
    this.$refs.mapRef.$mapPromise.then((map) => (this.map = map));
  },

  computed: {
    mapCoordinates() {
      if (!this.map) {
        // google map not inited
        return {
          lat: 0,
          lnt: 0,
        };
      }
      return {
        lat: this.map.getCenter().lat(),
        lng: this.map.getCenter().lng(),
      };
    },
  },
};
</script>