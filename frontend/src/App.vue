<template>
  <div class="grid h-full md:h-auto md:grid-cols-2 bg-slate-700">
    <!-- Left Section: Logos with Descriptions -->
    <div id="list" class="p-6 overflow-y-scroll h-screen sm:h-screen" ref="logosContainer">
      <!-- Search Bar -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search merchants..."
        class="w-full px-4 py-3 mb-6 rounded-lg bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-200"
      />
      <!-- Flex container for dropdowns -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-justify sm:text-sm mb-6">
        <!-- Dropdown for sorting by country -->
        <select 
          v-model="filterByCountry" 
          :disabled="showNearbyOnly"
          class="w-full px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border transition-all duration-200"
          :class="showNearbyOnly ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed' : 'bg-gray-50 text-gray-900 border-gray-200 hover:border-gray-300'"
        >
          <option value="default">Country: All</option>
          <option v-for="country in uniqueCountries" :key="country" :value="country">{{ country }}</option>
        </select>

        <!-- Dropdown for sorting by city -->
        <select 
          v-model="filterByCity" 
          :disabled="showNearbyOnly"
          class="w-full px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border transition-all duration-200"
          :class="showNearbyOnly ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed' : 'bg-gray-50 text-gray-900 border-gray-200 hover:border-gray-300'"
        >
          <option value="default">City: All</option>
          <option v-for="city in uniqueCities" :key="city" :value="city">{{ city }}</option>
        </select>

        <!-- Dropdown for sorting by category -->
        <select v-model="filterByCategory" class="w-full px-4 py-2 rounded-lg bg-gray-50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-200">
          <option value="default">Category: All</option>
          <option v-for="category in categoriesList" :key="category" :value="category.id">{{ category.name }}</option>
        </select>

        <!-- Dropdown for sorting by last transaction date -->
        <select v-model="filterByLastTransaction" class="w-full px-4 py-2 rounded-lg bg-gray-50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-200">
          <option value="default">Last Transaction: All</option>
          <option value="24hours">Within last 24 hours</option>
          <option value="1week">Within last 1 week</option>
          <option value="1month">Within last 1 month</option>
          <option value="3months">Within last 3 months</option>
          <option value="more">More than 3 months ago</option>
        </select>
      </div>
      
      <!-- Note about disabled filters when nearby is active -->
      <div v-if="showNearbyOnly" class="text-center mb-4">
        <p class="text-gray-400 text-xs">
          ℹ️ Country and city filters are disabled when showing nearby merchants
        </p>
      </div>

      <!-- Filter buttons -->
      <div class="flex items-center justify-center space-x-4 mb-4">
        <!-- Show Merchants Near Me Button -->
        <div class="flex space-x-2">
          <button 
            v-if="!showNearbyOnly"
            @click="showMerchantsNearMe" 
            class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200"
            :disabled="isGettingLocation"
          >
            <svg v-if="!isGettingLocation" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <div v-if="isGettingLocation" class="animate-spin rounded-full h-4 w-4 inline mr-2 border-t-2 border-b-2 border-white"></div>
            {{ isGettingLocation ? 'Getting Location...' : 'Show Merchants Near Me' }}
          </button>
          
          <!-- Clear Nearby Filter Button -->
          <button 
            v-if="showNearbyOnly"
            @click="clearNearbyFilter" 
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Clear Nearby Filter
          </button>
        </div>
        
        <button 
          @click="toggleUnverifiedFilter" 
          class="px-4 py-2 text-sm font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200"
          :class="showUnverified ? 'text-white bg-blue-600 hover:bg-blue-700 focus:ring-blue-500' : 'text-blue-600 bg-blue-100 hover:bg-blue-200 focus:ring-blue-500'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ showUnverified ? 'Hide Unverified Merchants' : 'Show Unverified Merchants' }}
        </button>
      </div>

      <!-- Merchants count and status -->
      <div class="text-center mb-6">
        <p class="text-white text-lg font-medium">{{ filteredMerchants.length }} merchants</p>
        <p v-if="showNearbyOnly && userLocation" class="text-green-400 text-sm mt-1">
          📍 Showing merchants within 10km of your location
        </p>
      </div>

      <!-- Grid for logos with descriptions -->
      <div v-if="!isLoading" class="mt-2 grid grid-cols-1 md:grid-cols-2 w-85 md-270 lg-255 h-auto md-auto">
        <!-- Logos with descriptions -->
        <div v-for="(merchant, index) in paginatedMerchants" :key="merchant.id" 
          class="flex flex-col p-4 m-2 rounded-lg bg-slate-300 hover:bg-gray-100 transition-all duration-300 transform hover:scale-[1.02] shadow-sm border border-gray-200"
          :style="showUnverified ? (merchant.verified ? 'border-top: 4px solid #10B981' : 'border-top: 4px solid #EF4444') : ''"
          @click="showPopup(merchant)">
          <!-- Check if merchant.logo is defined before accessing its url property -->
          <div class="h-full">
            <img v-if="merchant.logo" :src="merchant.logo" :alt="merchant.name + ' Logo'" class="m-auto sm:h-auto md:h-20 w-20 md-50 lg-75 object-fill cursor-pointer float-right" style="padding-left: 12px;">
            <div class="text-sm md:text-xs">
              <h3 class="text-lg font-semibold text-gray-900">{{ merchant.name }}</h3>
              <template v-if="merchant.town">
                <p class="text-gray-600">{{ merchant.town }}, {{ merchant.province }}, {{ merchant.country }}</p>
              </template>
              <template v-else>
                <p class="text-gray-600">{{ merchant.city }}, {{ merchant.country }}</p>
              </template>
              <p class="text-gray-600" v-if="merchant.last_transaction_date">Last transaction: {{ formatDate(merchant.last_transaction_date) }}</p>
            </div>
          </div>
                      <p class="mt-2 text-white flex items-center space-x-3">
              <a v-if="getGoogleMapLink(merchant)" :href="getGoogleMapLink(merchant)" target="_blank" class="inline-flex items-center text-green-400 hover:text-green-300 transition-colors duration-200" title="View in Google Maps">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
              </a>
              <a v-if="merchant.website_url" :href="merchant.website_url" target="_blank" class="inline-flex items-center text-blue-400 hover:text-blue-300 transition-colors duration-200" title="Visit Website">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
              </a>
            </p>
        </div>
      </div>

      <!-- Loading Spinner -->
      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>

      <!-- Load More Button -->
      <div v-if="!reachedEnd && filteredMerchants.length > pageSize && initialRenderComplete" class="flex justify-center mt-6 mb-4">
        <button 
          @click="loadMoreMerchants" 
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-all duration-200"
        >
          Load More Merchants
        </button>
      </div>

      <!-- "You reached the end" text -->
      <div v-if="reachedEnd" class="flex items-center justify-center mt-4 text-gray-500">
        <p>You reached the end</p>
      </div>

    </div>

    <!-- Right Section: Map  -->
    <div id="map" class="sm:block h-screen w-full">
      <MapView ref="mapView" :merchants="filteredMerchants" />
    </div>

    <!-- Button to toggle map visibility -->
    <div v-if="initialRenderComplete" class="fixed bottom-4 left-4 md:left-8 md:bottom-8 md:hidden" style="z-index: 9999;">
      <button @click="toggleMapView" class="px-6 py-3 ml-2 bg-blue-500 text-white rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-200 shadow-md font-semibold text-lg inline-flex items-center">
        <svg v-if="currentView === 'map'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        {{ currentView === 'map' ? 'Back to List' : 'Show Map' }}
      </button>
    </div>

  </div>

</template>

<script>
import axios from 'axios';
import MapView from '@/components/MapView.vue';
import moment from 'moment';

const DOMAIN = 'https://map.paytaca.com'

// Default map center
const defaultCenter = [11.2441900, 124.9987370]; // Tacloban City
// const defaultCenter = [-2.745453205711577, 129.97266776311113]; // Custom

export default {
  name: 'App',
  components: {
    MapView,
  },
  data() {
    return {
      merchants: [],
      mapCenter: defaultCenter,
      zoomLevel: 5,
      searchQuery: '',
      filterByCountry: 'default', // Default value for filtering by country dropdown
      filterByCity: 'default', // Default value for filtering by city dropdown
      filterByCategory: 'default', // Default value for filtering by category dropdown
      filterByLastTransaction: 'default', // Default value for filtering by last transaction dropdown
      currentPage: 1,
      pageSize: 15,
      categoriesList: [], // List to store categories
      reachedEnd: false, // Flag to indicate whether the end of scroll is reached
      currentView: 'list',
      merchantsFilter: null,
      showUnverified: false,
      isLoading: true,
      initialRenderComplete: false, // Add new state variable
      isGettingLocation: false, // Track location permission state
      userLocation: null, // Store user's current location
      showNearbyOnly: false // Track if we're showing nearby merchants only
    };
  },
  async mounted() {
    await this.fetchCategories(); // Fetch categories on component mount
    this.$refs.logosContainer.addEventListener('scroll', this.handleScroll);
    console.log("Scroll event listener added.");
    
    if (this.isMobile) {
      const mapElement = document.getElementById('map');
      if (mapElement) {
        mapElement.style.display = 'none';
      }
    }

    let urlParams = new URLSearchParams(window.location.search)
    if (urlParams.has('merchants')) {
      this.merchantsFilter = urlParams.get('merchants')
    }
    if (urlParams.has('category')) {
      const categoryShortName = urlParams.get('category')
      // Find the category in categoriesList by short_name
      const category = this.categoriesList.find(cat => cat.short_name === categoryShortName)
      if (category) {
        this.filterByCategory = category.id
      }
    }
    await this.fetchMerchants();
  },
  beforeUnmount() {
    this.$refs.logosContainer.removeEventListener('scroll', this.handleScroll);
    console.log("Scroll event listener removed.");
  },
  computed: {
    isMobile () {
      return /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) || window.innerWidth < 768
    },
    // Filtered merchants based on search query, country, category, last transaction date, and nearby location
    filteredMerchants() {
      return this.merchants.filter(merchant => {
        // Check if the merchant matches the search query
        const matchesSearchQuery = !this.searchQuery || merchant.name.toLowerCase().includes(this.searchQuery.toLowerCase());

        // Check if the merchant matches the selected country
        const matchesCountry = this.filterByCountry === 'default' || merchant.country === this.filterByCountry;

        // Check if the merchant matches the selected city
        const matchesCity = this.filterByCity === 'default' || merchant.city === this.filterByCity;

        // Check if the merchant matches the selected last transaction filter
        const matchesLastTransaction = this.checkLastTransaction(merchant.last_transaction_date);

        // Check verification status
        const matchesVerification = this.showUnverified || merchant.verified;

        // Check if merchant is within 10km radius when showing nearby merchants
        let matchesNearby = true;
        if (this.showNearbyOnly && this.userLocation && merchant.latitude && merchant.longitude) {
          const distance = this.calculateDistance(
            this.userLocation.latitude, 
            this.userLocation.longitude, 
            merchant.latitude, 
            merchant.longitude
          );
          matchesNearby = distance <= 10; // Within 10km
        }

        // Return true only if all filters match
        return matchesSearchQuery && matchesCountry && matchesCity && matchesLastTransaction && matchesVerification && matchesNearby;
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
    
    // List of unique cities for city dropdown options (filtered by selected country)
    uniqueCities() {
      const cities = new Set();
      this.merchants.forEach(merchant => {
        // Only include cities from the selected country, or all cities if no country is selected
        if (merchant.city && (this.filterByCountry === 'default' || merchant.country === this.filterByCountry)) {
          cities.add(merchant.city);
        }
        // if (merchant.town) {
        //   cities.add(merchant.town);
        // }
      });
      return Array.from(cities).sort(); // Sort the city names alphabetically
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
      let url = DOMAIN + '/api/merchants/'
      const params = new URLSearchParams()
      
      if (this.merchantsFilter) {
        params.append('filter_by_id', this.merchantsFilter)
      }
      
      if (this.filterByCategory !== 'default') {
        params.append('category_id', this.filterByCategory)
      }
      
      const queryString = params.toString()
      if (queryString) {
        url += '?' + queryString
      }
      
      this.isLoading = true; // Set loading state to true before API call
      axios.get(url)
        .then(response => {
          const merchants = response.data;
          this.fetchLocations(merchants);
        })
        .catch(error => {
          console.error('Error fetching merchants:', error);
          this.isLoading = false; // Set loading state to false on error
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
              merchant.town = location.town;
              merchant.city = location.city;
              merchant.province = location.province;
              merchant.state = location.state;
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
          this.isLoading = false; // Set loading state to false on error
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
          this.isLoading = false;
          // Use nextTick to ensure DOM is updated before showing the button
          this.$nextTick(() => {
            setTimeout(() => {
              this.initialRenderComplete = true;
            }, 100); // Small delay to ensure smooth transition
          });
        })
        .catch(error => {
          console.error('Error fetching logos:', error);
          this.isLoading = false;
          this.initialRenderComplete = true; // Still show content even if there's an error
        });
    },

    fetchCategories() {
      return axios.get(DOMAIN + '/api/categories/')
        .then(response => {
          const categories = response.data;
          this.categoriesList = categories.map(category => ({
            id: category.id,
            name: category.name,
            short_name: category.short_name
          }));
          return this.categoriesList; // Return the categories for await
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
          return []; // Return empty array on error
        });
    },
    getGoogleMapLink(merchant) {
      if (merchant.gmap_business_link) {
        return merchant.gmap_business_link
      } else {
        return `https://www.google.com/maps?q=${merchant.latitude},${merchant.longitude}`
      }
    },
    showPopup(merchant) {

      this.zoomLevel = 17.5
      
      if (this.isMobile) {
        this.toggleMapView();
      }

      console.log('X', merchant.last_transaction_date)
      const transactionDate = new Date(merchant.last_transaction_date);
      console.log('Y', transactionDate)
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
      if (merchant.last_transaction_date) {
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
      }

      let popupContent = `<div class="rounded-lg"><div class="flex items-center justify-between"><h3 class='text-lg font-semibold text-gray-900'>${merchant.name}</h3>`;
      
      // Include merchant logo if available
      if (merchant.logo) {
        popupContent += `<img src="${merchant.logo}" alt="${merchant.name} Logo" class="h-16 w-16 rounded-full">`;
      }
      
      popupContent += `</div><div>`;
      
      // Include merchant information if available
      if (merchant.city) {
        popupContent += `<p>${merchant.city}, ${merchant.country}</p>`;
      } else if (merchant.town) {
        popupContent += `<p>${merchant.town}, ${merchant.province}, ${merchant.country}</p>`;
      }
       
      // Include last transaction time if available
      if (timeText) {
        popupContent += `<p>Last transaction: ${timeText}</p>`;
      }
      
      // Include link to Google Map
      popupContent += `<div class="flex items-center"><a href="${this.getGoogleMapLink(merchant)}" target="_blank" class="inline-flex items-center px-3 py-2 text-xs font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200" style="color: white;">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
        View in Google Map
      </a></div>`;

      // Include website link if available
      if (merchant.website_url) {
        const buttonText = merchant.categories?.some(cat => cat.short_name === 'hiverooms') ? 'Book Now' : 'Visit Website';
        popupContent += `<div class="mt-3"><a href="${merchant.website_url}" target="_blank" class="inline-flex items-center px-3 py-2 text-xs font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200" style="color: white;">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
          </svg>
          ${buttonText}
        </a></div>`;
      }

      popupContent += `</div></div></div>`;
      
      // Open popup at merchant coordinates with the popup content
      this.$refs.mapView.openPopup(merchant.latitude, merchant.longitude, popupContent);
      
      // Center the map on the merchant coordinates
      this.$refs.mapView.centerOnTarget([merchant.latitude, merchant.longitude], this.zoomLevel);
    },
    handleScroll() {
      const container = this.$refs.logosContainer;
      // Add a small buffer (10px) to ensure we trigger before reaching absolute bottom
      const scrollPosition = container.scrollTop + container.clientHeight;
      const scrollHeight = container.scrollHeight - 100;
      
      // Check if we've scrolled to the bottom (with buffer)
      if (scrollPosition >= scrollHeight) {
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

      // Reset loading flag to false after loading is complete
      this.loading = false;
    },
    showListView() {
      this.currentView = 'list';
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

      if (this.isMobile && this.currentView === 'map') {
        // When switching to map view on mobile, fit the viewport properly
        this.$refs.mapView.fitViewportWhenVisible();
      }
      // Don't update map when switching to list view - let it stay where it is
    },
    checkLastTransaction(transactionDate) {
      if (this.filterByLastTransaction === 'default') {
        return true; // Return true for all merchants if no filter applied
      }

      const date = new Date(transactionDate);
      const currentDate = new Date();
      const timeDifference = currentDate - date;

      switch (this.filterByLastTransaction) {
        case '24hours':
          return timeDifference < 24 * 60 * 60 * 1000; // Last 24 hours
        case '1week':
          return timeDifference < 7 * 24 * 60 * 60 * 1000; // Last 1 week
        case '1month':
          return date > moment().subtract(1, 'months');
        case '3months':
        return date > moment().subtract(4, 'months');
        case 'more':
        return date <= moment().subtract(4, 'months');
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
    },
    
    // Calculate distance between two coordinates using Haversine formula
    calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371; // Earth's radius in kilometers
      const dLat = this.deg2rad(lat2 - lat1);
      const dLon = this.deg2rad(lon2 - lon1);
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      const distance = R * c; // Distance in kilometers
      return distance;
    },
    
    // Convert degrees to radians
    deg2rad(deg) {
      return deg * (Math.PI/180);
    },
    
    // Show merchants within 10km of user location
    showMerchantsNearMe() {
      this.isGettingLocation = true;
      
      if (!navigator.geolocation) {
        alert('Geolocation is not supported by this browser.');
        this.isGettingLocation = false;
        return;
      }
      
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          this.userLocation = { latitude, longitude };
          this.showNearbyOnly = true;
          
          // Reset other filters when showing nearby merchants
          this.filterByCountry = 'default';
          this.filterByCity = 'default';
          this.filterByCategory = 'default';
          this.filterByLastTransaction = 'default';
          
          this.isGettingLocation = false;
        },
        (error) => {
          this.isGettingLocation = false;
          switch(error.code) {
            case error.PERMISSION_DENIED:
              alert('Location permission denied. Please enable location access in your browser settings.');
              break;
            case error.POSITION_UNAVAILABLE:
              alert('Location information unavailable. Please try again.');
              break;
            case error.TIMEOUT:
              alert('Location request timed out. Please try again.');
              break;
            default:
              alert('An unknown error occurred while getting your location.');
              break;
          }
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000
        }
      );
    },
    
    // Clear the nearby filter and show all merchants
    clearNearbyFilter() {
      this.showNearbyOnly = false;
      this.userLocation = null;
      this.filterByCountry = 'default';
      this.filterByCity = 'default';
      this.filterByCategory = 'default';
      this.filterByLastTransaction = 'default';
    },
    
    // Toggle the unverified merchants filter
    toggleUnverifiedFilter() {
      this.showUnverified = !this.showUnverified;
    }
  },
  watch: {
    searchQuery(newValue, oldValue) {
      // Reset current page to 1 when search query changes
      if (newValue !== oldValue) {
        this.currentPage = 1;
        this.reachedEnd = false; // Reset the flag when search query changes

        // Reset all dropdowns when search query changes
        this.filterByCountry = 'default';
        this.filterByCity = 'default';
        this.filterByCategory = 'default';
        this.filterByLastTransaction = 'default';
        // Also reset nearby filter when search query changes
        this.showNearbyOnly = false;
        this.userLocation = null;
      }
    },
    filterByCountry(newValue) {
      if (newValue !== 'default') {
        // For any country selection, use default values and let MapView auto-fit to markers
        this.mapCenter = defaultCenter;
        this.zoomLevel = 3.5;
        
        // Reset city filter when country changes
        this.filterByCity = 'default';
        
        // Only update map if map view is currently active
        if (this.currentView === 'map' && !this.isMobile) {
          this.$refs.mapView.centerOnTarget(this.mapCenter, this.zoomLevel);
        }
      } else {
        this.mapCenter = defaultCenter;
        this.zoomLevel = 3.5;
        
        // Reset city filter when country is reset to default
        this.filterByCity = 'default';
        
        // Only update map if map view is currently active
        if (this.currentView === 'map' && !this.isMobile) {
          this.$refs.mapView.centerOnTarget(this.mapCenter, this.zoomLevel);
        }
      }
    },
    filterByCity(newValue) {
      if (newValue !== 'default') {
        // For any city selection, use default values and let MapView auto-fit to markers
        this.mapCenter = defaultCenter;
        this.zoomLevel = 3.5;
        
        // Only update map if map view is currently active
        if (this.currentView === 'map' && !this.isMobile) {
          this.$refs.mapView.centerOnTarget(this.mapCenter, this.zoomLevel);
        }
      }
    },
    filterByCategory(newValue) {
      if (newValue !== 'default') {
        this.fetchMerchants();
      }
    },
    filterByLastTransaction(newValue) {
      if (newValue !== 'default') {
        // Keep other filters active, just update the last transaction filter
        this.fetchMerchants();
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

/* button:hover:not(:disabled) {
  background-color: #e2e8f0;
} */

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
