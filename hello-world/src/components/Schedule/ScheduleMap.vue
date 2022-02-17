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
        v-for="(marker, index) in markers"
        :position="marker.position"
        @click="markerClicked(marker)"
      >
        <GmapInfoWindow
          :opened="marker.infoWindowShown"
          @closeclick="marker.infoWindowShown = false"
        >
          <v-card max-width="250" flat>
            <v-img height="120" :src="marker.url"></v-img>

            <v-card-title>{{ marker.name }}</v-card-title>

            <v-card-text>
              <v-row align="center" class="mx-0">
                <v-rating
                  :value="4.5"
                  color="amber"
                  dense
                  half-increments
                  readonly
                  size="14"
                ></v-rating>

                <div class="grey--text ms-4">4.5 (413)</div>
              </v-row>

              <div class="my-4 text-subtitle-1">$ • Italian, Cafe</div>

              <div>
                Small plates, salads & sandwiches - an intimate setting with 12
                indoor seats plus patio seating.
              </div>
            </v-card-text>
          </v-card>
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
import { gmapApi } from "vue2-google-maps";

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
      googlePlacesService: null,
    };
  },

  methods: {
    setPlace(place) {
      this.currentPlace = place;
    },
    addMarker(place) {
      if (this.currentPlace) {
        const { place_id } = place;

        console.log(place);

        const marker = {
          lat: this.currentPlace.geometry.location.lat(),
          lng: this.currentPlace.geometry.location.lng(),
        };
        this.userCoordinates = marker;
        this.markers.push({
          position: marker,
          infoWindowShown: false,
          place_id: place_id,
          url: place.photos[0].getUrl(),
          name: place.name,
        });
        this.currentPlace = null;
      }
    },

    markerClicked(marker) {
      this.markers.forEach((e) => (e.infoWindowShown = false)); // closed every other infowindow

      this.center = marker.position; // open this window
      marker.infoWindowShown = true;

      // this.markers = [...this.markers]; // trigger v-model binding
    },

    showPlaceOnMap(place) {
      const { name } = place;

      const request = {
        query: name,
        fields: ["name", "geometry", "place_id", "photo"],
      };
      const service = this.getGooglePlacesService();
      service.findPlaceFromQuery(request, (results, status) => {
        if (
          status === this.google.maps.places.PlacesServiceStatus.OK &&
          results
        ) {
          const { place_id } = results[0];

          if (this.markers.filter((e) => e.place_id === place_id).length > 0)
            return; // markers already contain this place

          this.setPlace(results[0]);
          this.addMarker(results[0]);

          this.map.setCenter(results[0].geometry.location);
        }
      });

      // service.getDetails(request, (results, status) => {
      //   if (
      //     status === this.google.maps.places.PlacesServiceStatus.OK &&
      //     results
      //   ) {
      //     // for (let i = 0; i < results.length; i++) {
      //     this.setPlace(results[0]);
      //     this.addMarker(place_id);
      //     // }
      //     this.map.setCenter(results[0].geometry.location);
      //   }
      // });
    },

    hidePlaceOnMap(place) {
      const { name } = place;

      const request = {
        query: name,
        fields: ["name", "place_id"],
      };

      const service = this.getGooglePlacesService();
      service.findPlaceFromQuery(request, (results, status) => {
        if (
          status === this.google.maps.places.PlacesServiceStatus.OK &&
          results
        ) {
          const { place_id } = results[0];
          this.markers = this.markers.filter((e) => e.place_id !== place_id);
        }
      });
    },

    getGooglePlacesService() {
      if (this.googlePlacesService !== null) return this.googlePlacesService;

      return new this.google.maps.places.PlacesService(this.map);
    },
  },

  created() {
    this.$root.$on("show-place-on-map", this.showPlaceOnMap); // register hook for SchedulePlacesCard.vueow
    this.$root.$on("hide-place-on-map", this.hidePlaceOnMap); // register hook for SchedulePlacesCard.vue

    this.$gmapApiPromiseLazy(); // init google api
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