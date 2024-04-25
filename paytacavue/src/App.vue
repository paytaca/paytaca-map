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
        class="w-full px-4 py-2 mb-4 rounded-lg bg-gray-light text-gray-dark focus:outline-none"
      />

      <!-- Flex container for dropdowns -->
      <div class="flex mb-4">
        <!-- Dropdown for sorting by country -->
        <select v-model="sortBy" class="flex-1 px-4 py-2 mr-2 rounded-lg bg-gray-light text-gray-dark focus:outline-none">
          <option value="default">All Country</option>
          <option v-for="country in uniqueCountries" :key="country" :value="country">{{ country }}</option>
        </select>

        <!-- Dropdown for sorting by category -->
        <select v-model="sortByCategory" class="flex-1 px-4 py-2 rounded-lg bg-gray-light text-gray-dark focus:outline-none">
          <option value="default">All Categories</option>
          <option v-for="category in uniqueCategories" :key="category" :value="category">{{ category }}</option>
        </select>
      </div>

      <!-- Grid for logos with descriptions -->
      <div class="mt-2 grid grid-cols-1 md:grid-cols-3 w-85 md-270 lg-255 h-auto md-auto">
        <!-- Logos with descriptions -->
        <div v-for="(merchant, index) in paginatedMerchants" :key="merchant.id" class="flex flex-col border-2 border-y-gray-dark p-2 m-2 rounded-3xl bg-gray-light" @click="showPopup(merchant)">
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

      <!-- Pagination -->
      <div class="flex items-center justify-center mt-4 space-x-2">
        <button @click="previousPage" :disabled="currentPage === 1" :class="{ 'opacity-50': currentPage === 1 }" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md focus:outline-none focus:ring focus:ring-gray-300">
          Previous
        </button>
        <template v-for="pageNumber in visiblePageNumbers" :key="pageNumber">
          <button @click="gotoPage(pageNumber)" :class="{ 'bg-blue-500 text-white': pageNumber === currentPage, 'bg-gray-200 text-gray-700': pageNumber !== currentPage }" class="px-4 py-2 rounded-md focus:outline-none focus:ring focus:ring-gray-300">
            {{ pageNumber }}
          </button>
        </template>
        <button @click="nextPage" :disabled="currentPage === totalPages" :class="{ 'opacity-50': currentPage === totalPages }" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md focus:outline-none focus:ring focus:ring-gray-300">
          Next
        </button>
      </div>
    </div>

    <!-- Right Section: Map (hidden on small screens) -->
    <div class="hidden sm:block h-screen w-full">
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
      sortBy: 'default', // Default value for sorting by country dropdown
      sortByCategory: 'default', // Default value for sorting by category dropdown
      currentPage: 1,
      pageSize: 9,
      categoriesMap: new Map(), // Map to store categories for each merchant
    };
  },
  mounted() {
    this.fetchMerchants();
    this.fetchCategories(); // Fetch categories on component mount
  },
  computed: {
    // Filtered merchants based on search query, country, and category
    filteredMerchants() {
      let filtered = this.merchants.filter(merchant => {
        return merchant.name.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
      if (this.sortBy !== 'default') {
        filtered = filtered.filter(merchant => merchant.country === this.sortBy);
      }
      if (this.sortByCategory !== 'default') {
        filtered = filtered.filter(merchant => {
          const categories = this.categoriesMap.get(merchant.id);
          return categories && categories.includes(this.sortByCategory);
        });
      }
      return filtered;
    },
    // List of unique countries for country dropdown options
    uniqueCountries() {
      const countries = new Set();
      this.merchants.forEach(merchant => {
        if (merchant.country) { // Check if country value is defined
          countries.add(merchant.country);
        }
      });
      return Array.from(countries).sort(); // Sort the country names alphabetically
    },
    // List of unique categories for category dropdown options
    uniqueCategories() {
      const categories = new Set();
      this.merchants.forEach(merchant => {
        const merchantCategories = this.categoriesMap.get(merchant.id);
        if (merchantCategories) {
          merchantCategories.forEach(category => categories.add(category));
        }
      });
      return Array.from(categories).sort(); // Sort the category names alphabetically
    },
    // Paginated merchants based on filtered results
    paginatedMerchants() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      return this.filteredMerchants.slice(startIndex, startIndex + this.pageSize);
    },
    totalPages() {
      return Math.ceil(this.filteredMerchants.length / this.pageSize);
    },
    visiblePageNumbers() {
      const pageCount = Math.ceil(this.filteredMerchants.length / this.pageSize);
      const pages = [];
      for (let i = 1; i <= pageCount; i++) {
        pages.push(i);
      }
      return pages;
    },
  },
  methods: {
    fetchMerchants() {
      axios.get('http://localhost:8000/merchants/')
        .then(response => {
          const merchants = response.data;
          this.fetchLocations(merchants);
        })
        .catch(error => {
          console.error('Error fetching merchants:', error);
        });
    },
    fetchLocations(merchants) {
      axios.get('http://localhost:8000/locations/')
        .then(response => {
          const locations = response.data;
          const locationMap = new Map();
          locations.forEach(location => {
            locationMap.set(location.merchant, location);
          });
          merchants.forEach(merchant => {
            const location = locationMap.get(merchant.id);
            if (location) {
              merchant.location = location.location;
              merchant.city = location.city;
              merchant.country = location.country;
              merchant.latitude = location.latitude;
              merchant.longitude = location.longitude;
            }
          });
          this.merchants = merchants;
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
    fetchCategories() {
      axios.get('http://localhost:8000/categories/')
        .then(response => {
          const categories = response.data;
          categories.forEach(category => {
            if (!this.categoriesMap.has(category.merchant)) {
              this.categoriesMap.set(category.merchant, []);
            }
            this.categoriesMap.get(category.merchant).push(category.category);
          });
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
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

      let popupContent = `<div class="flex items-center justify-between"><div><h3 class='font-semibold'>${merchant.name}</h3>`;

      // Include merchant logo if available
      if (merchant.logo) {
        popupContent += `<img src="${merchant.logo}" alt="${merchant.name} Logo" class="h-16 w-16 rounded-full">`;
      }

      popupContent += `</div><div>`;
      
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

      popupContent += `</div></div>`;

      // Open popup at merchant coordinates with the popup content
      this.$refs.mapView.openPopup(merchant.latitude, merchant.longitude, popupContent);

      // Center the map on the merchant coordinates
      this.$refs.mapView.setCenter(merchant.latitude, merchant.longitude);
    },
    setCurrentPage(pageNumber) {
      this.currentPage = pageNumber;
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    gotoPage(pageNumber) {
      this.currentPage = pageNumber;
    }
  }
};
</script>

<style scoped>
/* Additional Styles for Pagination */
.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.space-x-2 > * + * {
  margin-left: 0.5rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.bg-gray-200 {
  background-color: #edf2f7;
}

.text-gray-700 {
  color: #4a5568;
}

.rounded-md {
  border-radius: 0.375rem;
}

.focus\:outline-none:focus {
  outline: none;
}

.focus\:ring:focus {
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
}

.opacity-50 {
  opacity: 0.5;
}

/* Button hover styles */
button:hover {
  cursor: pointer;
}

button:hover:not(:disabled) {
  background-color: #e2e8f0;
}

/* Active button styles */
button:active:not(:disabled) {
  background-color: #cbd5e0;
}

/* Disabled button styles */
button:disabled {
  cursor: not-allowed;
}
</style>
