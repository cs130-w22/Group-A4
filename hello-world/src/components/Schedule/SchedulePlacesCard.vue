<template>
  <v-item-group multiple>
    <div class="text-h4 mb-1 text-center" v-text="'Places to visit'"></div>
    <v-row dense>
      <v-col v-for="(item, i) in items" :key="i" cols="12">
        <v-item v-slot="{ active, toggle }">
          <v-card
            :color="active ? 'primary' : 'grey'"
            class="d-flex align-center ma-1"
            dark
            height="200"
            @click="toggle"
          >
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title
                  class="text-h5"
                  v-text="item.title"
                ></v-card-title>
                <v-card-subtitle v-text="item.subtitle"></v-card-subtitle>
              </div>
              <v-avatar class="ma-3" size="125" tile>
                <v-img :src="item.src"></v-img>
              </v-avatar>
            </div>

            <v-scroll-y-transition>
              <!-- <div v-if="active" class="text-h2 flex-grow-1 text-center">
                added
              </div> -->
            </v-scroll-y-transition>
          </v-card>
        </v-item>
      </v-col>
    </v-row>
  </v-item-group>
</template>


<script>
// Todo: use google places api here
// import axios from "axios";

export default {
  name: "SchedulePlacesCard",
  data: () => ({
    items: [
      {
        src: "https://itin-dev.sfo2.cdn.digitaloceanspaces.com/freeImage/doG5bfmYNq6xrPLci3QZldd508cnd9uc",
        title: "The High Line",
        subtitle:
          "Popular park 30 feet above street level on an old rail line, with river & city views.",
      },
      {
        src: "https://itin-dev.sfo2.cdn.digitaloceanspaces.com/freeImage/IqF0JB0T0DeIdYVfUxhJEy5oM3QlZha6",
        title: "Statue of Liberty National Monument",
        subtitle:
          "Iconic National Monument opened in 1886, offering guided tours, a museum & city views.",
      },
    ],
  }),

  mounted() {
    //   const apikey = "AIzaSyCrt7b1kPOg4J7ayO6IgIJfy6R_9vp5Rlw";
    //   const url = `https://maps.googleapis.com/maps/api/place/photo
    // ?maxwidth=400
    // &photo_reference=Aap_uEA7vb0DDYVJWEaX3O-AtYp77AaswQKSGtDaimt3gt7QCNpdjp1BkdM6acJ96xTec3tsV_ZJNL_JP-lqsVxydG3nh739RE_hepOOL05tfJh2_ranjMadb3VoBYFvF0ma6S24qZ6QJUuV6sSRrhCskSBP5C1myCzsebztMfGvm7ij3gZT
    // &key=${apikey}`;
    //   axios
    //     .get(url)
    //     .then((resp) => {
    //       console.log(resp);
    //     })
    //     .catch((err) => {
    //       console.log(err.response);
    //     });
  },
};
</script>