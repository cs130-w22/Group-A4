<template>
  <v-menu bottom min-width="200px" rounded offset-y>
    <template v-slot:activator="{ on }">
      <v-btn icon x-large v-on="on">
        <v-avatar color="brown" size="48">
          <span class="white--text text-h5">{{ initials }}</span>
        </v-avatar>
      </v-btn>
    </template>
    <v-card>
      <v-list-item-content class="justify-center">
        <div class="mx-auto text-center">
          <v-avatar color="brown">
            <span class="white--text text-h5">{{ initials }}</span>
          </v-avatar>
          <h3>{{ fullName }}</h3>
          <p class="text-caption mt-1">
            {{ email }}
          </p>
          <v-divider class="my-3"></v-divider>
          <v-btn depressed rounded text v-on:click="signOut"> Sign out </v-btn>
        </div>
      </v-list-item-content>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: "UserPanel",
  props: ["user"],
  // data: () => ({
  //   user: {
  //     initials: "JD",
  //     fullName: "John Doe",
  //     email: "john.doe@doe.com",
  //   },
  // }),

  computed: {
    fullName() {
      if (!this.user) return "";
      return this.user.first_name + " " + this.user.last_name;
    },
    initials() {
      if (!this.user) return "";

      return this.user.first_name[0] + this.user.last_name[0];
    },
    email() {
      if (!this.user) return "";

      return this.user.email;
    },
  },

  methods: {
    signOut() {
      this.$emit("sign-out");
    },
  },
};
</script>