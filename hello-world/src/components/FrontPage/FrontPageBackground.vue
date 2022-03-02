<template>
  <v-img
    class="align-center mx-auto"
    height="90vh"
    width="100%"
    src="https://images.unsplash.com/photo-1549106765-3d312a9425e1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1752&q=80"
    position="25% 100%"
  >
    <div class="website_title" v-text="'Lazy Trip'"></div>
    <div
      class="website_subtitle"
      v-text="'Explore the world without the hassles'"
    ></div>

    <div v-on:keyup.enter="onEnter($event)">
      <vuetify-google-autocomplete
        id="map"
        ref="autocomplete"
        types="(cities)"
        v-on:placechanged="getAddressData"
        :error-messages="errorMessages"
        :error="errorMessages.length > 0"
        prefix="A trip to"
        solo
        shaped
        return-object
        style="max-width: 30%"
        class="mx-auto"
      >
      </vuetify-google-autocomplete>
    </div>
    <!-- <v-text-field
      v-model="query"
      v-on:keyup.enter="onEnter"
      @click:append="onEnter"
      :error-messages="errorMessages"
      :error="errorMessages.length > 0"
      prefix="A trip to"
      append-icon="mdi-magnify"
      solo
      shaped
      style="max-width: 30%"
      class="mx-auto"
    ></v-text-field> -->
  </v-img>
</template>

<script>
export default {
  name: "FrontPageBackground",
  data: () => ({
    errorMessages: [],
    address: null,
  }),

  methods: {
    getAddressData(address) {
      this.address = address;
    },
    onEnter() {
      setTimeout(() => {
        if (this.address === null) {
          this.showErrorMessage("Select from the dropdown and press enter");
          return;
        }
        this.$router.push({
          name: "schedule",
          params: {
            location:
              this.address.name +
              "," +
              this.address.administrative_area_level_1 +
              "," +
              this.address.country,
          },
        });
        this.address = null;
        this.$refs.autocomplete.clear();
      }, 100);
    },

    showErrorMessage(errorMessages) {
      this.errorMessages = [errorMessages];
      setTimeout(() => {
        this.errorMessages = [];
      }, 3000);
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Caveat&family=Fuzzy+Bubbles:wght@700&family=Rubik+Mono+One&display=swap");
</style>

<style>
.website_title {
  font-family: "Bungee Shade", "Caveat", sans-serif;
  font-size: 60px;
  font-weight: bold;
  text-align: center;
}
.website_subtitle {
  font-family: "Caveat", sans-serif;
  font-size: 25px;
  text-align: center;
}
.error--text {
  animation: v-shake 0.6s cubic-bezier(0.25, 0.8, 0.5, 1);
}
</style>
