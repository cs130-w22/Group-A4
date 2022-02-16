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
      >
      <GmapInfoWindow>

<v-card
    max-width="250"
    flat
  >
    <v-img
      height="120"
      src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
    ></v-img>

    <v-card-title>Cafe Badilico</v-card-title>

    <v-card-text>
      <v-row
        align="center"
        class="mx-0"
      >
        <v-rating
          :value="4.5"
          color="amber"
          dense
          half-increments
          readonly
          size="14"
        ></v-rating>

        <div class="grey--text ms-4">
          4.5 (413)
        </div>
      </v-row>

      <div class="my-4 text-subtitle-1">
        $ • Italian, Cafe
      </div>

      <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio seating.</div>
    
    </v-card-text>
</v-card>

        <!-- <div class="ui header">{{ m.name }}</div>
         <p>{{ m.vicinity}} </p> -->

      

      </GmapInfoWindow>
      </GmapMarker>
    </GmapMap>

    <v-toolbar
      dense
      floating
      style="
        position: absolute;
        top: 20px;
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
          >
          </v-text-field>
        </template>
      </gmap-autocomplete>
      <button class="btn" @click="addMarker">Add</button>
    </v-toolbar>
  </v-card>
</template>

<script>
import {gmapApi} from 'vue2-google-maps'

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
        // console.log(this.currentPlace)
        this.markers.push({ position: marker, });
        this.userCoordinates = marker;
        this.currentPlace = null;
      }
    },

    showPlaceOnMap(place){

      this.$gmapApiPromiseLazy().then(() => {
            const request = {
              query: place,
              fields: ["name", "geometry"],
            };
          const service = new this.google.maps.places.PlacesService(this.map);
          service.findPlaceFromQuery(request, (results, status) => {
            if (status === this.google.maps.places.PlacesServiceStatus.OK && results) {
              for (let i = 0; i < results.length; i++) {
                this.setPlace(results[i]);
                this.addMarker();
              }
              this.map.setCenter(results[0].geometry.location);
            }
          });
      })
    }
  },

  created() {
    this.$root.$on('show-place-on-map', this.showPlaceOnMap); // register hook for SchedulePlacesCard.vue

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
    google: gmapApi,
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