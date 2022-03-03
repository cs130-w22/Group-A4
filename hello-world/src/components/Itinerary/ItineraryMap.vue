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
      ref="itineraryMap"
    >
      <GmapMarker
        v-for="marker in markers"
        :key="marker.place_id"
        :position="marker.position"
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
  name: "ItineraryMap",
  data() {
    return {
      map: null,
      userCoordinates: {
        lat: 34.05,
        lng: -118.24,
      },
      zoom: 12,
      currentPlace: null,
      markers: [],
      googlePlacesService: null,
    };
  },

  methods: {
    setPlace(place) {
      this.currentPlace = place;
    },
    async addMarker(place) {
      if (this.markers.some((e) => e.place_id === place.place_id)) return;

      if (place) {
        let placeDetail = await this.getPlaceDetails(place);

        const marker = {
          lat: placeDetail.geometry.location.lat(),
          lng: placeDetail.geometry.location.lng(),
        };
        this.userCoordinates = marker;
        const placeObj = placeDetail;
        placeObj.position = marker;
        placeObj.infoWindowShown = true;
        try {
          placeObj.review = placeDetail.reviews[0].text;
          placeObj.photo_url = await placeDetail.photos[0].getUrl();
        } catch (err) {
          placeObj.review = "No review"; // google api fails to return anything useful
        }

        this.markers.forEach((e) => (e.infoWindowShown = false));
        this.markers.push(placeDetail);
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
      const markersFound = this.markers.filter(
        (e) => e.place_id === place.place_id
      );

      if (markersFound.length > 0) {
        // clicked a marker that is present, change its state
        this.markerClicked(markersFound[0]);
      } else {
        // clicked a marker that is not present
        this.addMarker(place); // add marker first
      }
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
        // console.log(results);
        // console.log(status);
        alert("You clicked too fast");

        return Promise.reject(results);
      }
    },

    removeAllMarkers() {
      this.markers = [];
    },

    getGooglePlacesService() {
      if (this.googlePlacesService !== null) return this.googlePlacesService;

      return new this.google.maps.places.PlacesService(this.map);
    },
  },

  created() {
    this.$gmapApiPromiseLazy(); // init google api

    this.$root.$on("show-place-on-itinerary-map", this.showPlaceOnMap); // register hook for ItineraryTimeline.vue
    // this.$root.$on("hide-place-on-itinerary-map", this.hidePlaceOnMap); // register hook for ItineraryTimeline.vue
    // this.$root.$on("add-marker-on-itinerary-map", this.addMarker);

    this.$root.$on(
      "remove-all-markers-on-itinerary-map",
      this.removeAllMarkers
    );
  },

  mounted() {
    this.$refs.itineraryMap.$mapPromise.then((map) => (this.map = map));
  },

  computed: {
    google: gmapApi,
  },
};
</script>