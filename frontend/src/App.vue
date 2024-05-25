<template>
  <div class="grid h-full md:h-auto md:grid-cols-2 bg-bg-dark">
    <!-- Left Section: Logos with Descriptions -->
    <div id="list" class="p-4 overflow-y-scroll h-screen sm:h-screen" ref="logosContainer">

      <!-- Search Bar -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search merchants..."
        class="w-full px-4 py-2 mb-4 rounded-lg bg-gray-light text-gray-dark focus:outline-none"
      />

      <!-- Text view for displaying the number of search results -->
      <p class="text-gray-700 mb-2">Displaying {{ filteredMerchants.length }} of {{ merchants.length }} merchants</p>

      <!-- Flex container for dropdowns -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-2 text-justify sm:text-sm">
        <!-- Dropdown for sorting by country -->
        <select v-model="sortBy" class="px-4 py-2 rounded-lg bg-gray-light text-gray-dark focus:outline-none">
          <option value="default">All Countries</option>
          <option v-for="country in uniqueCountries" :key="country" :value="country">{{ country }}</option>
        </select>

        <!-- Dropdown for sorting by category -->
        <select v-model="sortByCategory" class="px-4 py-2 rounded-lg bg-gray-light text-gray-dark focus:outline-none">
          <option value="default">All Categories</option>
          <option v-for="category in uniqueCategories" :key="category" :value="category">{{ category }}</option>
        </select>

        <!-- Dropdown for sorting by last transaction date -->
        <select v-model="sortByLastTransaction" class="px-4 py-2 rounded-lg bg-gray-light text-gray-dark focus:outline-none">
          <option value="default">Last Transaction</option>
          <option value="24hours">Last 24 Hours</option>
          <option value="1week">Last 1 Week</option>
          <option value="1month">Last 1 Month</option>
          <option value="3months">Last 3 Months</option>
          <option value="more">More than 3 Months</option>
        </select>
      </div>

      <!-- Grid for logos with descriptions -->
      <div class="mt-2 grid grid-cols-1 md:grid-cols-3 w-85 md-270 lg-255 h-auto md-auto">
        <!-- Logos with descriptions -->
        <div v-for="(merchant, index) in paginatedMerchants" :key="merchant.id" class="flex flex-col p-2 m-2 rounded-3xl bg-gray-light" :class="{ 'pointer-events-none': isMobile }" @click="showPopup(merchant)">
          <!-- Check if merchant.logo is defined before accessing its url property -->
          <img v-if="merchant.logo" :src="merchant.logo" :alt="merchant.name + ' Logo'" class="sm:h-auto md:h-44 w-25 md-50 lg-75 rounded-2xl object-fill cursor-pointer">
          <div class="text-sm md:text-xs">
            <h3 class="text-lg font-semibold italic">{{ merchant.name }}</h3>
            <p class="text-gray-800">{{ merchant.city }}, {{ merchant.country }}</p>
            <p class="text-gray-800">Last transaction: {{ formatDate(merchant.last_transaction_date) }}</p>
          </div>
        </div>
      </div>

      <!-- "You reached the end" text -->
      <div v-if="reachedEnd" class="flex items-center justify-center mt-4 text-gray-700">
        <p>You reached the end</p>
      </div>

    </div>

    <!-- Right Section: Map  -->
    <div id="map" class="hidden sm:block sm:m-4 h-screen w-full">
      <MapView ref="mapView" :merchants="filteredMerchants" />
    </div>

    <!-- Button to toggle map visibility -->
    <div class="fixed bottom-4 left-4 md:left-8 md:bottom-8 md:hidden" style="z-index: 9999;">
      <button @click="toggleMapView" class="px-4 py-2 ml-2 bg-gray-light text-gray-dark rounded-md focus:outline-none focus:ring focus:ring-gray-300">
        {{ currentView === 'map' ? 'Show List' : 'Show Map' }}
      </button>
    </div>

  </div>

</template>

<script>
import axios from 'axios';
import MapView from '@/components/MapView.vue';

const DOMAIN = 'https://map.paytaca.com'

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
      sortByLastTransaction: 'default', // Default value for sorting by last transaction dropdown
      currentPage: 1,
      pageSize: 9,
      categoriesMap: new Map(), // Map to store categories for each merchant
      reachedEnd: false, // Flag to indicate whether the end of scroll is reached
      currentView: 'list',
      isMobile: window.innerWidth < 768
    };
  },
  mounted() {
    this.fetchMerchants();
    this.fetchCategories(); // Fetch categories on component mount
    this.$refs.logosContainer.addEventListener('scroll', this.handleScroll);
    console.log("Scroll event listener added.");
  },
  beforeDestroy() {
    this.$refs.logosContainer.removeEventListener('scroll', this.handleScroll);
    console.log("Scroll event listener removed.");
  },
  computed: {
    // Filtered merchants based on search query, country, category, and last transaction date
    filteredMerchants() {
      return this.merchants.filter(merchant => {
        // Check if the merchant matches the search query
        const matchesSearchQuery = !this.searchQuery || merchant.name.toLowerCase().includes(this.searchQuery.toLowerCase());

        // Check if the merchant matches the selected country
        const matchesCountry = this.sortBy === 'default' || merchant.country === this.sortBy;

        // Check if the merchant matches the selected category
        const matchesCategory = this.sortByCategory === 'default' ||
          (this.categoriesMap.has(merchant.id) && this.categoriesMap.get(merchant.id).includes(this.sortByCategory));

        // Check if the merchant matches the selected last transaction filter
        const matchesLastTransaction = this.filterByLastTransaction(merchant.last_transaction_date);

        // Return true only if all filters match
        return matchesSearchQuery && matchesCountry && matchesCategory && matchesLastTransaction;
      });
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
      return this.filteredMerchants.slice(0, this.pageSize);
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
      axios.get(DOMAIN + '/api/merchants/')
        .then(response => {
          const merchants = response.data;
          this.fetchLocations(merchants);
        })
        .catch(error => {
          console.error('Error fetching merchants:', error);
        });
    },
    fetchLocations(merchants) {
      axios.get(DOMAIN + '/api/locations/')
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
      axios.get(DOMAIN + '/api/logos/')
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
      axios.get(DOMAIN + '/api/categories/')
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

      // Convert milliseconds to years, months, weeks, days, hours, and minutes
      const years = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365));
      const months = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 30));
      const weeks = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 7));
      const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
      const hours = Math.floor(timeDifference / (1000 * 60 * 60));
      const minutes = Math.floor(timeDifference / (1000 * 60));

      // Choose the appropriate time unit based on the duration
      if (years > 0) {
        timeText = years === 1 ? '1 year ago' : `${years} years ago`;
      } else if (months > 0) {
        timeText = months === 1 ? '1 month ago' : `${months} months ago`;
      } else if (weeks > 0) {
        timeText = weeks === 1 ? '1 week ago' : `${weeks} weeks ago`;
      } else if (days > 0) {
        timeText = days === 1 ? '1 day ago' : `${days} days ago`;
      } else if (hours > 0) {
        timeText = hours === 1 ? '1 hour ago' : `${hours} hours ago`;
      } else {
        timeText = minutes === 1 ? '1 minute ago' : `${minutes} minutes ago`;
      }

      let popupContent = `<div class="rounded-lg"><div class="flex items-center justify-between"><h3 class='font-semibold'>${merchant.name}</h3>`;
      
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
      
      popupContent += `</div></div></div>`;
      
      // Open popup at merchant coordinates with the popup content
      this.$refs.mapView.openPopup(merchant.latitude, merchant.longitude, popupContent);
      
      // Center the map on the merchant coordinates
      this.$refs.mapView.setCenter(merchant.latitude, merchant.longitude);
    },
    handleScroll() {
      const container = this.$refs.logosContainer;
      // Check if the user has scrolled to the bottom of the container
      if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
        // Load more merchants
        console.log("Reached bottom of container. Loading more merchants...");
        this.loadMoreMerchants();
      }
    },
    loadMoreMerchants() {
      // Check if the page is already loading
      if (this.loading) {
        return; // Exit the function if the page is already loading
      }

      // Set loading flag to true to indicate that the page is loading
      this.loading = true;

      // Increase the pageSize by 9 to load more merchants
      this.pageSize += 9;

      // Check if all merchants are loaded
      if (this.pageSize >= this.filteredMerchants.length) {
        this.reachedEnd = true; // Set the flag to indicate the end of scroll
      }

      // For smaller screens (SM), automatically load more merchants when reaching the bottom
      if (window.innerWidth < 320) { // Adjust the breakpoint as needed
        const container = this.$refs.logosContainer;
        // Check if the user has scrolled to the bottom of the container
        if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
          // Load more merchants
          console.log("Reached bottom of container. Loading more merchants...");
          // Update the loading flag to false before calling loadMoreMerchants() recursively
          this.loading = false;
          this.loadMoreMerchants();
        }
      }

      // Reset loading flag to false after loading is complete
      this.loading = false;
    },
    showListView() {
      this.currentView = 'list';
    },
    showMapView() {
      // Toggle the map view regardless of screen size
      this.currentView = 'map';
    },
    toggleMapView() {
      // Toggle between 'list' and 'map' views
      this.currentView = this.currentView === 'map' ? 'list' : 'map';

      // Update visibility of list and map based on currentView
      const listElement = document.getElementById('list');
      const mapElement = document.getElementById('map');

      if (this.currentView === 'list') {
        listElement.style.display = 'block';
        mapElement.style.display = 'none';
      } else {
        listElement.style.display = 'none';
        mapElement.style.display = 'block';
      }
    },
    filterByLastTransaction(transactionDate) {
      if (this.sortByLastTransaction === 'default') {
        return true; // Return true for all merchants if no filter applied
      }

      const date = new Date(transactionDate);
      const currentDate = new Date();
      const timeDifference = currentDate - date;

      switch (this.sortByLastTransaction) {
        case '24hours':
          return timeDifference < 24 * 60 * 60 * 1000; // Last 24 hours
        case '1week':
          return timeDifference < 7 * 24 * 60 * 60 * 1000; // Last 1 week
        case '1month':
          return currentDate.getMonth() === date.getMonth() && currentDate.getFullYear() === date.getFullYear(); // Last 1 month
        case '3months':
          return currentDate.getMonth() - date.getMonth() < 3; // Last 3 months
        case 'more':
          return currentDate.getMonth() - date.getMonth() >= 3; // More than 3 months
        default:
          return true;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const currentDate = new Date();
      const timeDifference = currentDate - date;

      // Convert milliseconds to years, months, weeks, days, hours, and minutes
      const years = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365));
      const months = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 30));
      const weeks = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 7));
      const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
      const hours = Math.floor(timeDifference / (1000 * 60 * 60));
      const minutes = Math.floor(timeDifference / (1000 * 60));

      // Choose the appropriate time unit based on the duration
      if (years > 0) {
        return years === 1 ? '1 year ago' : `${years} years ago`;
      } else if (months > 0) {
        return months === 1 ? '1 month ago' : `${months} months ago`;
      } else if (weeks > 0) {
        return weeks === 1 ? '1 week ago' : `${weeks} weeks ago`;
      } else if (days > 0) {
        return days === 1 ? '1 day ago' : `${days} days ago`;
      } else if (hours > 0) {
        return hours === 1 ? '1 hour ago' : `${hours} hours ago`;
      } else {
        return minutes === 1 ? '1 minute ago' : `${minutes} minutes ago`;
      }
    }
  },
  watch: {
    searchQuery(newValue, oldValue) {
      // Reset current page to 1 when search query changes
      if (newValue !== oldValue) {
        this.currentPage = 1;
        this.reachedEnd = false; // Reset the flag when search query changes

        // Reset all dropdowns when search query changes
        this.sortBy = 'default';
        this.sortByCategory = 'default';
        this.sortByLastTransaction = 'default';
      }
    },
    sortBy(newValue, oldValue) {
      // Reset sortByCategory and sortByLastTransaction when sortBy changes
      if (newValue !== 'default') {
        this.sortByCategory = 'default';
        this.sortByLastTransaction = 'default';
      }
    },
    sortByCategory(newValue, oldValue) {
      // Reset sortBy and sortByLastTransaction when sortByCategory changes
      if (newValue !== 'default') {
        this.sortBy = 'default';
        this.sortByLastTransaction = 'default';
      }
    },
    sortByLastTransaction(newValue, oldValue) {
      // Reset sortBy and sortByCategory when sortByLastTransaction changes
      if (newValue !== 'default') {
        this.sortBy = 'default';
        this.sortByCategory = 'default';
      }
    },
  },
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

#vute{
  color: #000;
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

.pointer-events-none {
  pointer-events: none;
}

</style>
