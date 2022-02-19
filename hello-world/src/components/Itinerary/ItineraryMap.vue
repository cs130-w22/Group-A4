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
  name: "ItineraryMap",
  data() {
    return {
      map: null,
      userCoordinates: {
        lat: 0,
        lng: 0,
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
        // placeObj.zIndex = ++this.curZIndex;

        // this.markers.push({
        //   position: marker,
        //   infoWindowShown: true,
        //   place_id: place_id,
        //   // url: place.photos[0].getUrl(),
        //   name: place.name,
        //   rating: place.rating,
        //   price_level: place.price_level,
        //   zIndex: ++this.curZIndex,
        // });

        this.markers.forEach((e) => (e.infoWindowShown = false));
        this.markers.push(placeObj);
        // this.currentPlace = null;
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

      this.setPlace(place);
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