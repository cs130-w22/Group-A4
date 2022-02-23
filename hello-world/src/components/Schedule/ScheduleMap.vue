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
        disableDefaultUi: true,
      }"
      style="width: 100%; height: 100%"
      ref="mapRef"
    >
      <GmapMarker
        v-for="(marker, index) in markers"
        :key="marker.place_id"
        :position="marker.position"
        :label="(index + 1).toString()"
        @click="markerClicked(marker)"
      >
        <GmapInfoWindow
          :opened="marker.infoWindowShown"
          @closeclick="marker.infoWindowShown = false"
        >
          <v-card max-width="300" max-height="360" flat>
            <v-img height="120" :src="marker.photo_url"></v-img>

            <v-card-title>{{ marker.name }}</v-card-title>

            <v-card-text>
              <v-row align="center" class="mx-0">
                <v-rating
                  :value="marker.rating"
                  color="amber"
                  dense
                  half-increments
                  readonly
                  size="14"
                ></v-rating>

                <div class="grey--text ms-4">
                  {{ marker.rating }} ({{ marker.user_ratings_total }})
                </div>
              </v-row>

              <div class="my-4 text-subtitle-1">
                <span v-for="i in marker.price_level" :key="i">$</span>
                • {{ marker.types[0] }}, {{ marker.types[1] }}
              </div>

              <div>
                {{ marker.review }}
              </div>
            </v-card-text>
          </v-card>
        </GmapInfoWindow>
      </GmapMarker>
    </GmapMap>
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
      zoom: 12,
      markers: [],
      googlePlacesService: null,
      googleGeocoder: null,
    };
  },
  created() {
    this.$root.$on("show-place-on-map", this.showPlaceOnMap); // register hook for SchedulePlacesCard.vueow
    this.$root.$on("hide-place-on-map", this.hidePlaceOnMap); // register hook for SchedulePlacesCard.vue

    this.$gmapApiPromiseLazy().then(() => {
      this.setCityCoordinate(); // wait to use the geocoder service of google api
    });
  },
  mounted() {
    this.$refs.mapRef.$mapPromise.then((map) => (this.map = map));
  },
  watch: {
    location: {
      // do not need immediate because it is done by he created()
      handler(newLocation) {
        if (newLocation === undefined) return; // user leaving the tab

        this.setCityCoordinate();
      },
    },
  },
  computed: {
    google: gmapApi,
    location() {
      return this.$route.params.location;
    },
  },

  methods: {
    async addMarker(place) {
      if (this.markers.some((e) => e.place_id === place.place_id)) return; // markers already contain this place

      if (place) {
        const marker = {
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng(),
        };
        this.userCoordinates = marker;

        const placeObj = place;
        placeObj.position = marker;
        placeObj.infoWindowShown = true;
        const detail = await this.getPlaceDetails(place);

        try {
          placeObj.review = detail.reviews[0].text;
        } catch (err) {
          placeObj.review = "No review"; // google api fails to return anything useful
        }

        this.markers.forEach((e) => (e.infoWindowShown = false));
        this.markers.push(placeObj);
      }
    },

    markerClicked(marker) {
      const nextInfoWindowState = !marker.infoWindowShown;
      this.center = marker.position;
      this.markers.forEach((e) => (e.infoWindowShown = false));
      marker.infoWindowShown = nextInfoWindowState;

      this.markers = [...this.markers]; // trigger v-model binding
    },

    showPlaceOnMap(place) {
      if (typeof place.geometry.location.lat === "number") {
        const { lat, lng } = place.geometry.location;
        place.geometry.location.lat = function () {
          return lat;
        };

        place.geometry.location.lng = function () {
          return lng;
        };
      }

      this.addMarker(place);

      // this.getPlaceDetails(place);

      // const request = {
      //   query: name,
      //   fields: ["name", "geometry", "place_id", "photo"],
      // };
      // const service = this.getGooglePlacesService();
      // service.findPlaceFromQuery(request, (results, status) => {
      //   if (
      //     status === this.google.maps.places.PlacesServiceStatus.OK &&
      //     results
      //   ) {
      //     const { place_id } = results[0];

      //     this.setPlace(results[0]);
      //     this.addMarker(results[0]);

      //     this.map.setCenter(results[0].geometry.location);
      //   }
      // });
    },
    async setCityCoordinate() {
      const service = this.getGoogleGeocoder();

      const request = {
        address: this.location,
      };

      const { results, status } = await new Promise((resolve) =>
        service.geocode(
          request,
          // pass a callback to getDetails that resolves the promise
          (results, status) => resolve({ results, status })
        )
      );

      if (
        status === this.google.maps.GeocoderStatus.OK &&
        status !== this.google.maps.GeocoderStatus.ZERO_RESULTS
      ) {
        this.map.setCenter(results[0].geometry.location);
        return Promise.resolve(results);
      } else {
        return Promise.reject(results);
      }

      // service.geocode(request, (results, status) => {
      //   if (status === this.google.maps.GeocoderStatus.OK) {
      //     if (status !== this.google.maps.GeocoderStatus.ZERO_RESULTS) {
      //       console.log(results);
      //       this.map.setCenter(results[0].geometry.location);
      //     }
      //   }
      // });
    },

    async getPlaceDetails(place) {
      const { place_id } = place;
      const service = this.getGooglePlacesService();

      const request = {
        placeId: place_id,
      };

      const { results, status } = await new Promise((resolve) =>
        service.getDetails(
          request,
          // pass a callback to getDetails that resolves the promise
          (results, status) => resolve({ results, status })
        )
      );
      if (
        status === this.google.maps.places.PlacesServiceStatus.OK &&
        results
      ) {
        return Promise.resolve(results);
      } else {
        return Promise.reject(results);
      }
    },

    hidePlaceOnMap(place) {
      const { place_id } = place;
      this.markers = this.markers.filter((e) => e.place_id !== place_id);
    },

    getGooglePlacesService() {
      if (this.googlePlacesService !== null) return this.googlePlacesService;

      this.googlePlacesService = new this.google.maps.places.PlacesService(
        this.map
      );
      return this.googlePlacesService;
    },
    getGoogleGeocoder() {
      if (this.googleGeocoder !== null) return this.googleGeocoder;

      this.googleGeocoder = new this.google.maps.Geocoder();
      return this.googleGeocoder;
    },
  },
};
</script>