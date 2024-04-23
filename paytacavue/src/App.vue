<template>
  <div class="fixed">
      
  </div>
  <div class="grid h-screen md:h-auto md:grid-cols-2">
    <!-- Left Section: Logos with Descriptions -->
    <div class="p-4 overflow-y-scroll h-screen sm:h-screen">

      <!-- Search Bar -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search merchants..."
        class="w-full px-4 py-2 mb-4 rounded-lg bg-gray-light text-gray-dark focus:outline-none "
      />

      <div class="mt-2 grid grid-cols-1 md:grid-cols-3 w-85 md-270 lg-255 h-auto md-auto">
        <!-- Logos with descriptions -->
        <div v-for="merchant in filteredMerchants" :key="merchant.id" class="flex flex-col border-2 border-y-gray-dark p-2 m-2 rounded-3xl bg-gray-light" @click="showPopup(merchant)">
          <!-- Check if merchant.logo is defined before accessing its url property -->
          <img v-if="merchant.logo" :src="merchant.logo" :alt="merchant.name + ' Logo'" class="h-auto w-25 md-50 lg-75 rounded-2xl object-fill cursor-pointer">
          <div class="text-sm md:text-xs">
            <h3 class="text-lg font-semibold italic">{{ merchant.name }}</h3>
            <p class="text-gray-800">{{ merchant.location }}</p>
            <p class="text-gray-800">{{ merchant.city }}</p>
            <p class="text-gray-800">{{ merchant.country }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Section: Map -->
    <div class="h-screen w-full">
      <div id="map" class="h-screen"><MapView ref="mapView" :merchants="filteredMerchants" /></div>
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
      merchants: [],
      searchQuery: '',
    };
  },
  mounted() {
    this.fetchMerchants();
  },
  computed: {
    filteredMerchants() {
      return this.merchants.filter(merchant => {
        return merchant.name.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
  },
  methods: {
    fetchMerchants() {
      axios.get('http://localhost:8000/merchants/')
        .then(response => {
          const merchants = response.data;
          this.fetchLocations(merchants); // Fetch locations after fetching merchants
        })
        .catch(error => {
          console.error('Error fetching merchants:', error);
        });
    },
    fetchLocations(merchants) {
      axios.get('http://localhost:8000/locations/')
        .then(response => {
          const locations = response.data;
          // Map locations to merchants using merchant id
          const locationMap = new Map();
          locations.forEach(location => {
            locationMap.set(location.merchant, location);
          });
          // Associate locations with merchants
          merchants.forEach(merchant => {
            const location = locationMap.get(merchant.id);
            if (location) {
              merchant.location = location.location;
              merchant.city = location.city;
              merchant.country = location.country;
              merchant.latitude = location.latitude; // Updated
              merchant.longitude = location.longitude; // Updated
            }
          });
          // Set merchants data
          this.merchants = merchants;
          // After fetching merchants and locations, fetch logos for each merchant
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
          const logoMap = new Map();
          logos.forEach(logo => {
            if (!logoMap.has(logo.merchant)) {
              logoMap.set(logo.merchant, []);
            }
            logoMap.get(logo.merchant).push(logo.url);
          });
          this.merchants.forEach(merchant => {
            const logos = logoMap.get(merchant.id);
            merchant.logo = logos ? logos[0] : null;
          });
        })
        .catch(error => {
          console.error('Error fetching logos:', error);
        });
    },
    showPopup(merchant) {
  const transactionDate = new Date(merchant.last_transaction_date);
  const currentDate = new Date();
  const timeDifference = currentDate - transactionDate;
  let timeText = '';

  // Convert milliseconds to years, months, weeks, and days
  const years = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365));
  const months = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 30));
  const weeks = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 7));
  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

  // Choose the appropriate time unit based on the duration
  if (years > 0) {
    timeText = years === 1 ? '1 year ago' : `${years} years ago`;
  } else if (months > 0) {
    timeText = months === 1 ? '1 month ago' : `${months} months ago`;
  } else if (weeks > 0) {
    timeText = weeks === 1 ? '1 week ago' : `${weeks} weeks ago`;
  } else {
    timeText = days === 1 ? '1 day ago' : `${days} days ago`;
  }

  let popupContent = `<div><h3 class='font-semibold'>${merchant.name}</h3>`;

  // Include merchant information if available
  if (merchant.location && merchant.city && merchant.country) {
    popupContent += `<p>${merchant.location}, ${merchant.city}, ${merchant.country}</p>`;
  }

  // Include last transaction time if available
  if (timeText) {
    popupContent += `<p>Last transaction: ${timeText}</p>`;
  }

  // Include Google Maps link if available
  if (merchant.gmap_business_link) {
    popupContent += `<a href="${merchant.gmap_business_link}" target="_blank">View in Google Map</a>`;
  }

  popupContent += `</div>`;

  // Open popup at merchant coordinates with the popup content
  this.$refs.mapView.openPopup(merchant.latitude, merchant.longitude, popupContent);

  // Center the map on the merchant coordinates
  this.$refs.mapView.setCenter(merchant.latitude, merchant.longitude);
}
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>
