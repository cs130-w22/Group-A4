<template>
  <!-- <div class="panel"> -->
  <!-- <div class="panel-header text-center"> -->

  <!-- <v-avatar class="grey darken-3" size="60"> -->
  <span class="white--text"> {{ user.username }} </span>
  <!-- </v-avatar> -->
  <!-- <v-avatar color="teal" size="40">} </v-avatar> -->
  <!-- <div class="panel-title h5 mt-10">
        {{ user.first_name }} {{ user.last_name }}
      </div>
    </div>
  </div> -->
</template>

<script>
export default {
  name: "UserPanel",
  props: ["user"],
};
</script>