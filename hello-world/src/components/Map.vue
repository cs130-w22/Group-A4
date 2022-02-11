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
        <div class="text-h4 mb-1" v-text="'Your coordinates:'"></div>

        <p>
          {{ userCoordinates.lat }} Latitude,
          {{ userCoordinates.lng }} Longtitude
        </p>
      </div>

      <div>
        <div class="text-h4 mb-1" v-text="'Map coordinates:'"></div>
        <p>
          {{ mapCoordinates.lat }} Latitude, {{ mapCoordinates.lng }} Longtitude
        </p>
      </div>
    </div>

    <v-card class="pa-4" flat style="position: relative">
      <GmapMap
        :center="userCoordinates"
        :zoom="zoom"
        style="width: 80%; height: 300px; margin: 32px auto"
        ref="mapRef"
      >
      </GmapMap>

      <v-toolbar
        dense
        floating
        style="
          position: absolute;
          top: 60px;
          left: 50%;
          transform: translateX(-50%);
          z-index: 99;
        "
      >
        <v-text-field
          hide-details
          prepend-icon="mdi-magnify"
          single-line
        ></v-text-field>

        <v-btn icon>
          <v-icon>mdi-crosshairs-gps</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-toolbar>
    </v-card>
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