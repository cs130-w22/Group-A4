<template>
  <div>
    <v-card class="pa-4" flat style="position: relative">
      <GmapMap
        :center="userCoordinates"
        :zoom="zoom"
        :options="{
          mapTypeControl: false,
          scaleControl: false,
          streetViewControl: false,
          rotateControl: false,
          fullscreenControl: false,
          disableDefaultUi: false,
        }"
        style="width: 80%; height: 320px; margin: 32px auto"
        ref="mapRef"
      ></GmapMap>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "DemoMap",
  data() {
    return {
      map: null,
      userCoordinates: {
        lat: 0,
        lng: 0,
      },
      zoom: 4,
    };
  },
  created() {
    this.$getLocation({})
      .then((coordinates) => {
        this.userCoordinates = coordinates;
      })
      .catch((error) => console.log(error)); // users do not grant permission of the location
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