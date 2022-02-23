<template>
  <v-item-group multiple v-model="selected">
    <div
      class="text-h5 mt-4 text-center font-weight-bold"
      v-text="'Select the places you are interested in'"
    ></div>

    <v-row dense justify="center">
      <v-col cols="11">
        <v-toolbar dense flat>
          <gmap-autocomplete v-on:place_changed="setPlace" class="introInput">
            <template v-slot:input="slotProps">
              <v-text-field
                prepend-inner-icon="place"
                placeholder="Location Of Event"
                ref="input"
                v-on:listeners="slotProps.listeners"
                v-on:attrs="slotProps.attrs"
              >
              </v-text-field>
            </template>
          </gmap-autocomplete>
          <v-btn dark small @click="addMarker(currentPlace)">Add my own</v-btn>
        </v-toolbar>
      </v-col>
      <v-progress-linear
        reverse
        query
        :indeterminate="loading"
      ></v-progress-linear>

      <v-col v-for="place in places" :key="place.place_id" cols="11">
        <v-icon class="float-right" @click="removeCard(place)" color="error">
          mdi-close
        </v-icon>

        <v-item v-slot="{ active, toggle }">
          <v-card
            :color="active ? 'green darken-1' : 'grey'"
            class="d-flex align-center ma-1"
            dark
            height="150"
            @click="toggle"
            v-on:click="!active ? showPlace(place) : hidePlace(place)"
          >
            <v-img
              :src="place.photo_url"
              class="white--text align-end"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              height="90%"
            >
              <v-card-title v-text="place.name"></v-card-title>
            </v-img>
          </v-card>
        </v-item>
      </v-col>
    </v-row>
  </v-item-group>
</template>


<script>
import axios from "axios";

export default {
  name: "SchedulePlacesCard",
  data: () => ({
    places: [],
    selected: [],
    currentPlace: null,
    loading: true,
  }),

  computed: {
    location() {
      return this.$route.params.location;
    },
  },
  watch: {
    location(newLocation) {
      if (newLocation === undefined) return;

      // users enter new location
      this.getPlaceInfo();

      this.selected = [];
      for (const place of this.places) {
        this.removeCard(place); // remove all current cards
      }
    },
  },

  created() {
    this.getPlaceInfo();
  },

  methods: {
    getPlaceInfo() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:8000/trip/search/loc/", {
          headers: { "Content-Type": "application/json" },
          params: { location: this.location },
        })
        .then((resp) => {
          this.loading = false;
          this.places = resp.data;
        })
        .catch((err) => {
          console.log(err.response);
        });
    },
    showPlace(place) {
      this.$root.$emit("show-place-on-map", place);
    },
    hidePlace(place) {
      this.$root.$emit("hide-place-on-map", place);
    },
    removeCard(place) {
      this.$root.$emit("hide-place-on-map", place);
      this.places = this.places.filter((e) => e.place_id !== place.place_id);
    },

    setPlace(place) {
      this.currentPlace = place;
    },
    addMarker(place) {
      if (this.places.some((e) => e.place_id === place.place_id)) return; // places already contain this place
      const placeObj = place;
      if (!("photos" in placeObj)) {
        placeObj.photo_url =
          "https://lahousing.lacity.org/AAHR/Images/No_Image_Available.jpg";
      } else {
        placeObj.photo_url = place.photos[0].getUrl();
      }

      this.places.unshift(placeObj);
      this.$root.$emit("show-place-on-map", place);
    },
  },
};
</script>

<style>
.introInput {
  width: 18vw;
}
</style>