<template>
  <v-card flat style="height: 90vh">
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
      style="width: 100%; height: 100%"
      ref="mapRef"
    >
      <GmapMarker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        @click="center = m.position"
      />
    </GmapMap>

    <v-toolbar
      dense
      floating
      style="
        position: absolute;
        top: 60px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1;
      "
    >
      <gmap-autocomplete v-on:place_changed="setPlace" class="introInput">
        <template v-slot:input="slotProps">
          <v-text-field
            outlined
            prepend-inner-icon="place"
            placeholder="Location Of Event"
            ref="input"
            v-on:listeners="slotProps.listeners"
            v-on:attrs="slotProps.attrs"
          >
          </v-text-field>
        </template>
      </gmap-autocomplete>
      <button class="btn" @click="addMarker">Add</button>
    </v-toolbar>
  </v-card>
</template>

<script>
export default {
  name: "ScheduleMap",
  data() {
    return {
      map: null,
      userCoordinates: {
        lat: 0,
        lng: 0,
      },
      zoom: 8,
      currentPlace: null,
      markers: [],
    };
  },

  methods: {
    setPlace(place) {
      this.currentPlace = place;
    },
    addMarker() {
      if (this.currentPlace) {
        const marker = {
          lat: this.currentPlace.geometry.location.lat(),
          lng: this.currentPlace.geometry.location.lng(),
        };
        this.markers.push({ position: marker });
        this.userCoordinates = marker;
        this.currentPlace = null;
      }
    },
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