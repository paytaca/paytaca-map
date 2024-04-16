<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 bg-gray-900 h-screen">
    <!-- Left Section: Logos with Descriptions -->
    <div class="p-4 overflow-y-auto h-96 sm:h-full">
      <div class="mt-2  grid grid-cols-3 ">
        <!-- Logos with descriptions -->
        <div v-for="location in locations" :key="location.id" class="flex flex-col items-center border-2 p-2 m-2 rounded-3xl bg-slate-400">
          <!-- Check if location.logo is defined before accessing its url property -->
          <img v-if="location.logo" :src="location.logo.url" alt="Location Logo" class="h-40 w-60 rounded-full">
          <div class="">
            <h3 class="text-lg font-semibold">{{ location.name }}</h3>
            <p class="text-gray-500">{{ location.location }}</p>
            <p class="text-gray-500">{{ location.city }}</p>
            <p class="text-gray-500">{{ location.country }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Section: Map -->
    <div class="h-screen">
      <div id="map" class="h-screen"><MapView /></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MapView from '@/components/MapView.vue';

export default {
  name: 'App',
  components: {
    MapView,
  },
  data() {
    return {
      locations: [],
    };
  },
  mounted() {
    this.fetchLocations();
  },
  methods: {
    fetchLocations() {
      axios.get('http://localhost:8000/locations/')
        .then(response => {
          this.locations = response.data;
          // After fetching locations, fetch logos for each location
          this.fetchLogos();
        })
        .catch(error => {
          console.error('Error fetching locations:', error);
        });
    },
    fetchLogos() {
      // Fetch logos separately for each location to avoid N+1 queries
      this.locations.forEach(location => {
        axios.get(`http://localhost:8000/logos/?location=${location.id}`)
          .then(response => {
            // Assuming the response data contains a single logo for each location
            location.logo = response.data[0];
          })
          .catch(error => {
            console.error('Error fetching logos:', error);
          });
      });
    }
  }
};
</script>

<style scoped>
/* Adjusting the width of the left and right sections */
.w-70 {
  width: 70%;
}

.w-30 {
  width: 30%;
}

/* Ensuring that the map container takes up the entire height of the screen */
#map {
  height: 100%;
}
</style>
