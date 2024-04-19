<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 bg-gray-dark h-screen">
    <!-- Left Section: Logos with Descriptions -->
    <div class="p-4 overflow-y-auto h-96 sm:h-full">
      <!-- Search Bar -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search merchants..."
        class="w-full px-4 py-2 mb-4 rounded-lg bg-gray-light text-gray-dark focus:outline-none"
      />

      <div class="mt-2 grid grid-cols-1 sm:grid-cols-3">
        <!-- Logos with descriptions -->
        <div v-for="location in filteredLocations" :key="location.id" class="flex flex-col border-2 border-y-gray-dark p-2 m-2 rounded-3xl bg-gray-light" @click="showPopup(location)">
          <!-- Check if location.logo is defined before accessing its url property -->
          <img v-if="location.logo" :src="location.logo" :alt="location.name + ' Logo'" class="h-120 w-auto rounded-2xl object-fill cursor-pointer">
          <div class="text-sm text-">
            <h3 class="text-lg font-semibold italic">{{ location.name }}</h3>
            <p class="text-gray-800">{{ location.location }}</p>
            <p class="text-gray-800">{{ location.city }}</p>
            <p class="text-gray-800">{{ location.country }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Section: Map -->
    <div class="h-screen">
      <div id="map" class="h-screen"><MapView ref="mapView" :locations="filteredLocations" /></div>
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
      searchQuery: '',
    };
  },
  mounted() {
    this.fetchLocations();
  },
  computed: {
    filteredLocations() {
      return this.locations.filter(location => {
        return location.name.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
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
      axios.get('http://localhost:8000/logos/')
        .then(response => {
          const logos = response.data;
          // Filter logos to ensure they are of size 120x120
          const filteredLogos = logos.filter(logo => logo.size === '120x120');
          // Create a map of location IDs to logos for easy lookup
          const logoMap = filteredLogos.reduce((map, logo) => {
            if (!map.has(logo.location)) {
              map.set(logo.location, []);
            }
            map.get(logo.location).push(logo.url);
            return map;
          }, new Map());

          // Assign logos to locations
          this.locations.forEach(location => {
            const locationLogos = logoMap.get(location.id);
            // Assign the first logo to the location (you can modify this logic if needed)
            location.logo = locationLogos ? locationLogos[0] : null;
          });
        })
        .catch(error => {
          console.error('Error fetching logos:', error);
        });
    },
    showPopup(location) {
      const popupContent = `
        <div>
          <h3>${location.name}</h3>
          <p>${location.location}, ${location.city}, ${location.country}</p>
          <p>Last transaction: ${location.last_transaction_date}</p>
          <a href="${location.gmap_business_link}" target="_blank">View in Google Map</a>
        </div>
      `;

      // Set map view to the location coordinates
      this.$refs.mapView.setCenter(location.latitude, location.longitude);

      // Open popup at location coordinates with the popup content
      this.$refs.mapView.openPopup(location.latitude, location.longitude, popupContent);
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>
