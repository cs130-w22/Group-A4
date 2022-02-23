<template>
  <v-img
    class="align-center mx-auto"
    height="90vh"
    width="100%"
    src="https://images.unsplash.com/photo-1549106765-3d312a9425e1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1752&q=80"
    position="25% 100%"
  >
    <div class="text-h3 mb-1 text-center" v-text="'Lazy Trip'"></div>
    <div
      class="text-h5 mb-1 text-center"
      v-text="'Explore the world without the hassles'"
    ></div>
    <v-text-field
      v-model="query"
      v-on:keyup.enter="onEnter"
      label="Begin your next trip"
      prepend-inner-icon="mdi-magnify"
      solo
      shaped
      style="max-width: 30%"
      class="mx-auto"
    ></v-text-field>
  </v-img>
</template>

<script>
export default {
  name: "FrontPageBackground",
  data: () => ({
    query: null,
  }),

  methods: {
    onEnter() {
      this.$router.push({ name: "schedule", params: { location: this.query } });
    },
  },
};
</script>
