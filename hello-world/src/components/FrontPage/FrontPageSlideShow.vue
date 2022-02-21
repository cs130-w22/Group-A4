<template>
  <v-row justify="center" style="margin: 0">
    <v-col cols="11" style="height: 90vh">
      <v-chip-group>
        <div
          class="text-h6 mb-1"
          v-text="'Try some popular destinations'"
        ></div>
        <v-spacer></v-spacer>
        <v-chip v-for="place in places" :key="place.name">
          {{ place.name }}
        </v-chip>
      </v-chip-group>
      <v-carousel v-model="model" cycle height="45vh">
        <v-carousel-item
          v-for="place in places"
          :key="place.name"
          :src="place.img"
        >
          <v-card-title>{{ place.name }}</v-card-title>
        </v-carousel-item>
      </v-carousel>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "FrontPageSlideShow",
  data: () => ({
    model: null,
    places: [
      {
        id: 1,
        name: "NYC",
        img: "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80",
      },
      {
        id: 2,
        name: "Los Angeles",
        img: "https://images.unsplash.com/photo-1542737579-ba0a385f3b84?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=776&q=80",
      },
      {
        id: 3,
        name: "Hawaii",
        img: "https://images.unsplash.com/photo-1505852679233-d9fd70aff56d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80",
      },
      {
        id: 4,
        name: "San Francisco",
        img: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2532&q=80",
      },
      {
        id: 5,
        name: "Las Vegas",
        img: "https://images.unsplash.com/photo-1581351721010-8cf859cb14a4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80",
      },
      {
        id: 6,
        name: "Alaska",
        img: "https://images.unsplash.com/photo-1535025287458-e3badca98021?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1746&q=8",
      },
      {
        id: 7,
        name: "Miami",
        img: "https://images.unsplash.com/photo-1506966953602-c20cc11f75e3?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8bWlhbWl8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60",
      },
      {
        id: 8,
        name: "Chicago",
        img: "https://images.unsplash.com/photo-1494522855154-9297ac14b55f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y2hpY2Fnb3xlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60",
      },
      {
        id: 9,
        name: "Orlando",
        img: "https://images.unsplash.com/photo-1618945372420-2470ece5277c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80",
      },
    ],
  }),
};
</script>