<template>
  <v-item-group multiple>
    <div class="text-h4 mb-1 text-center" v-text="'Places to visit'"></div>
    <v-row dense>
      <v-col v-for="(place, i) in places" :key="i" cols="12">
        <v-item v-slot="{ active, toggle }">
          <v-card
            :color="active ? 'primary' : 'grey'"
            class="d-flex align-center ma-1"
            dark
            height="200"
            @click="toggle"
            v-on:click="!active ? showPlace(place) : hidePlace(place)"
          >
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title
                  class="text-h5"
                  v-text="place.name"
                ></v-card-title>
                <v-card-subtitle v-text="place.subtitle"></v-card-subtitle>
              </div>
              <v-avatar class="ma-3" size="125" tile>
                <v-img :src="place.src"></v-img>
              </v-avatar>
            </div>

            <!-- <v-scroll-y-transition>
              <div v-if="active" class="text-h2 flex-grow-1 text-center">
                added
              </div>
            </v-scroll-y-transition> -->
          </v-card>
        </v-item>
      </v-col>
    </v-row>
  </v-item-group>
</template>


<script>
export default {
  name: "SchedulePlacesCard",
  data: () => ({
    places: [
      {
        src: "https://itin-dev.sfo2.cdn.digitaloceanspaces.com/freeImage/doG5bfmYNq6xrPLci3QZldd508cnd9uc",
        name: "The High Line",
        subtitle:
          "Popular park 30 feet above street level on an old rail line, with river & city views.",
        place_id: "123",
      },
      {
        src: "https://itin-dev.sfo2.cdn.digitaloceanspaces.com/freeImage/IqF0JB0T0DeIdYVfUxhJEy5oM3QlZha6",
        name: "Statue of Liberty National Monument",
        subtitle:
          "Iconic National Monument opened in 1886, offering guided tours, a museum & city views.",
        place_id: "234",
      },
    ],
  }),

  methods: {
    showPlace(place) {
      this.$root.$emit("show-place-on-map", place);
    },
    hidePlace(place) {
      this.$root.$emit("hide-place-on-map", place);
    },
  },
};
</script>