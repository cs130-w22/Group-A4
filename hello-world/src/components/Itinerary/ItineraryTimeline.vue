<template>
  <v-card class="mx-auto">
    <v-card-title class="pa-2">
      <h3 class="text-h6 font-weight-light text-center grow">
        {{ timeline.title }}
      </h3>
    </v-card-title>
    <v-virtual-scroll
      :items="timeline.trip_event"
      item-height="500"
      height="70vh"
      bench="1"
    >
      <template v-slot="{ item }">
        {{ item }}
        <v-container class="fill-height">
          <v-row align="center">
            <strong
              class="display-1 font-weight-regular mr-4"
              style="margin-left: 54px"
              >8</strong
            >
            <v-col justify="end">
              <div class="title font-weight-light">Tuesday</div>
              <div class="text-uppercase font-weight-light">February 2015</div>
            </v-col>
          </v-row>
        </v-container>
        <v-card-text class="py-0">
          <v-timeline align-top dense>
            <v-timeline-item color="pink" small>
              <v-row class="pt-1">
                <v-col cols="3">
                  <strong>5pm</strong>
                </v-col>
                <v-col>
                  <strong>New Icon</strong>
                  <div class="text-caption">Mobile App</div>
                </v-col>
              </v-row>
            </v-timeline-item>

            <v-timeline-item color="teal lighten-3" small>
              <v-row class="pt-1">
                <v-col cols="3">
                  <strong>3-4pm</strong>
                </v-col>
                <v-col>
                  <strong>Design Stand Up</strong>
                  <div class="text-caption mb-2">Hangouts</div>
                  <v-avatar>
                    <v-img
                      src="https://avataaars.io/?avatarStyle=Circle&topType=LongHairFrida&accessoriesType=Kurt&hairColor=Red&facialHairType=BeardLight&facialHairColor=BrownDark&clotheType=GraphicShirt&clotheColor=Gray01&graphicType=Skull&eyeType=Wink&eyebrowType=RaisedExcitedNatural&mouthType=Disbelief&skinColor=Brown"
                    ></v-img>
                  </v-avatar>
                  <v-avatar>
                    <v-img
                      src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairFrizzle&accessoriesType=Prescription02&hairColor=Black&facialHairType=MoustacheMagnum&facialHairColor=BrownDark&clotheType=BlazerSweater&clotheColor=Black&eyeType=Default&eyebrowType=FlatNatural&mouthType=Default&skinColor=Tanned"
                    ></v-img>
                  </v-avatar>
                  <v-avatar>
                    <v-img
                      src="https://avataaars.io/?avatarStyle=Circle&topType=LongHairMiaWallace&accessoriesType=Sunglasses&hairColor=BlondeGolden&facialHairType=Blank&clotheType=BlazerSweater&eyeType=Surprised&eyebrowType=RaisedExcited&mouthType=Smile&skinColor=Pale"
                    ></v-img>
                  </v-avatar>
                </v-col>
              </v-row>
            </v-timeline-item>

            <v-timeline-item color="pink" small>
              <v-row class="pt-1">
                <v-col cols="3">
                  <strong>12pm</strong>
                </v-col>
                <v-col>
                  <strong>Lunch break</strong>
                </v-col>
              </v-row>
            </v-timeline-item>

            <v-timeline-item color="teal lighten-3" small>
              <v-row class="pt-1">
                <v-col cols="3">
                  <strong>9-11am</strong>
                </v-col>
                <v-col>
                  <strong>Finish Home Screen</strong>
                  <div class="text-caption">Web App</div>
                </v-col>
              </v-row>
            </v-timeline-item>
          </v-timeline>
        </v-card-text>
      </template>
    </v-virtual-scroll>
    <!-- </div> -->
  </v-card>
</template>
<script>
export default {
  name: "ItineraryTimeline",
  props: ["timeline"],

  computed: {},

  created() {
    // this.timeline.trip_event
    // console.log(this.timeline);
  },

  methods: {},
};
</script>