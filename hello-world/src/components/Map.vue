<template>
    <div>
        <h1>Your coordinates:</h1>
        <p>{{ coordinates.lat }} Latitude, {{coordinates.lng }} Longtitude </p>
        <gmap-map
        :center="{lat:10, lng:10}"
        :zoom="7"
        map-type-id="terrain"
        style="width: 500px; height: 300px"
        >
        </gmap-map>>
            
    </div>
</template>

<script>
export default {
    name: 'GoogleMap',
    data() {
        return {
            coordinates: {
                lat : 0,
                lng : 0
            }
        }
    },

    created(){
        this.$getLocation({})
            .then(coordinates=>{
                this.coordinates = coordinates;
            }).catch(error => alert(error));
    }
}
</script>