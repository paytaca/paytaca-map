<template>
  <div class="min-h-screen md:grid md:h-auto md:grid-cols-2 bg-slate-700 overflow-x-hidden">
    <!-- Left Section: Logos with Descriptions -->
    <div id="list" class="p-6 md:overflow-y-scroll md:h-screen" ref="logosContainer" :class="{ 'hidden': isMobile && currentView === 'map' }">
      <!-- Search Bar -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search merchants..."
        class="w-full px-4 py-3 mb-6 rounded-lg bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-200"
      />

      <!-- Filter buttons -->
      <div class="flex items-center justify-start md:justify-center gap-2 mb-4 overflow-x-auto md:overflow-x-visible overflow-y-hidden flex-nowrap md:flex-wrap">
        <!-- Show Merchants Near Me Button -->
        <button 
          v-if="!showNearbyOnly"
          @click="showMerchantsNearMe" 
          class="px-3 md:px-4 py-2 text-xs md:text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 whitespace-nowrap flex-shrink-0"
          :disabled="isGettingLocation"
        >
          <svg v-if="!isGettingLocation" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <div v-if="isGettingLocation" class="animate-spin rounded-full h-4 w-4 inline mr-2 border-t-2 border-b-2 border-white"></div>
          {{ isGettingLocation ? 'Getting Location...' : 'Merchants Near Me' }}
        </button>
        
        <!-- Clear Nearby Filter Button -->
        <button 
          v-if="showNearbyOnly"
          @click="clearNearbyFilter" 
          class="px-3 md:px-4 py-2 text-xs md:text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200 whitespace-nowrap flex-shrink-0"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          Clear Nearby Filter
        </button>
        
        <button 
          @click="toggleUnverifiedFilter" 
          class="px-3 md:px-4 py-2 text-xs md:text-sm font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 whitespace-nowrap flex-shrink-0"
          :class="showUnverified ? 'text-white bg-blue-600 hover:bg-blue-700 focus:ring-blue-500' : 'text-blue-600 bg-blue-100 hover:bg-blue-200 focus:ring-blue-500'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ showUnverified ? 'Hide Non-Verified' : 'With Non-Verified' }}
        </button>

        <!-- More Filters Button -->
        <button 
          @click="showFilters = !showFilters" 
          class="px-3 md:px-4 py-2 text-xs md:text-sm font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 whitespace-nowrap flex-shrink-0"
          :class="showFilters ? 'text-white bg-purple-600 hover:bg-purple-700 focus:ring-purple-500' : 'text-purple-600 bg-purple-100 hover:bg-purple-200 focus:ring-purple-500'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          {{ showFilters ? 'Hide Filters' : 'More Filters' }}
        </button>
      </div>

      <!-- Flex container for dropdowns -->
      <div v-if="showFilters" class="grid grid-cols-2 md:grid-cols-4 gap-4 text-justify sm:text-sm mb-6">
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
      <div v-if="showNearbyOnly && showFilters" class="text-center mb-4">
        <p class="text-gray-400 text-xs">
          ℹ️ Country and city filters are disabled when showing nearby merchants
        </p>
      </div>

      <!-- Merchants count and status -->
      <div class="text-center mb-6">
        <p class="text-white text-lg font-medium">
          <span v-if="isLoading">Loading merchants...</span>
          <span v-else>{{ filteredMerchants.length }} merchants</span>
        </p>
        <p v-if="showNearbyOnly && userLocation" class="text-green-400 text-sm mt-1">
          📍 Showing merchants within 10km of your location
        </p>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="isLoading" class="mt-2 grid grid-cols-1 md:grid-cols-2 w-85 md-270 lg-255 h-auto md-auto">
        <div v-for="n in 8" :key="n"
          class="flex flex-col p-4 m-2 rounded-lg bg-slate-300 animate-pulse border border-gray-200">
          <div class="h-full flex gap-2">
            <div class="text-sm md:text-xs flex-1">
              <div class="h-5 bg-gray-400 rounded w-3/4 mb-2"></div>
              <div class="h-4 bg-gray-400 rounded w-1/2 mb-1"></div>
              <div class="h-3 bg-gray-400 rounded w-2/3 mt-2"></div>
            </div>
            <div class="w-20 h-20 bg-gray-400 rounded flex-shrink-0"></div>
          </div>
          <div class="mt-2 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="h-5 w-5 bg-gray-400 rounded-full"></div>
              <div class="h-5 w-5 bg-gray-400 rounded-full"></div>
            </div>
            <div class="h-6 w-8 bg-gray-400 rounded"></div>
          </div>
        </div>
      </div>

      <!-- Grid for logos with descriptions -->
      <div v-if="!isLoading" class="mt-2 grid grid-cols-1 md:grid-cols-2 w-85 md-270 lg-255 h-auto md-auto">
        <!-- Logos with descriptions -->
        <div v-for="merchant in paginatedMerchants" :key="merchant.id" 
          :data-merchant-id="merchant.id"
          class="flex flex-col p-4 m-2 rounded-lg bg-slate-300 hover:bg-gray-100 transition-all duration-300 transform hover:scale-[1.02] shadow-sm border-2 cursor-pointer relative"
          :class="{
            'border-blue-600 ring-4 ring-blue-400 bg-blue-100 shadow-lg shadow-blue-200 scale-[1.02] z-10': highlightedMerchantId === merchant.id,
            'border-gray-200': highlightedMerchantId !== merchant.id
          }"
          :style="showUnverified ? (merchant.verified ? 'border-top: 4px solid #10B981' : 'border-top: 4px solid #EF4444') : ''"
          @click="showPopup(merchant)">
          <!-- Highlight indicator badge -->
          <div v-if="highlightedMerchantId === merchant.id" class="absolute -top-2 -right-2 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded-full shadow-md z-20">
            Current
          </div>
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
          <div class="mt-2 flex items-center justify-between">
            <div class="flex items-center space-x-3">
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
              <span v-if="hasCashbackCampaign(merchant)" 
                    class="gift-icon inline-flex items-center text-yellow-400 animate-gift cursor-pointer" 
                    title="Click to view cashback details"
                    :ref="`gift-${merchant.id}`"
                    @click.stop="showCashbackDialog(merchant)">🎁</span>
            </div>
            <span class="text-xl">{{ getCountryFlag(merchant.country) }}</span>
          </div>
        </div>
      </div>

      <!-- Load More Button -->
      <div v-if="!reachedEnd && filteredMerchants.length > pageSize && initialRenderComplete && !isLoading && !isFetchingMerchants" class="flex justify-center mt-6 mb-4">
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
    <div id="map" class="h-screen w-full relative" :class="{ 'hidden': isMobile && currentView === 'list' }">
      <MapView ref="mapView" :merchants="filteredMerchants" />
      
      <!-- Explore Merchants Button -->
      <div v-if="!exploreClicked" class="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-[9999]">
        <button 
          @click="exploreRecentMerchants" 
          class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-300 whitespace-nowrap"
        >
          Explore Merchants
        </button>
      </div>
      
      <!-- Recently Active Merchants Label and Next Button -->
      <div 
        v-if="exploreClicked && showRecentLabel" 
        class="absolute bottom-8 left-8 z-[9999] transition-opacity duration-500 flex items-center gap-3"
        :class="{ 'opacity-0': !showRecentLabel, 'opacity-100': showRecentLabel }"
      >
        <span class="px-4 py-2 bg-white/90 backdrop-blur-sm text-gray-800 font-medium rounded-lg shadow-lg text-sm">
          Recently Active Merchants
        </span>
        <button 
          @click="goToNextRecentMerchant"
          class="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 text-sm whitespace-nowrap"
        >
          Next →
        </button>
      </div>
    </div>

    <!-- Button to toggle map visibility - Back to List on top left -->
    <div v-if="initialRenderComplete && currentView === 'map'" class="fixed top-4 left-4 md:hidden" style="z-index: 9999;">
      <button @click="toggleMapView" class="px-6 py-3 bg-blue-500 text-white rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-200 shadow-md font-semibold text-lg inline-flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to List
      </button>
    </div>

    <!-- Button to toggle map visibility - Show Map on bottom left -->
    <div v-if="initialRenderComplete && currentView === 'list'" class="fixed bottom-4 left-4 md:hidden" style="z-index: 9999;">
      <button @click="toggleMapView" class="px-6 py-3 bg-blue-500 text-white rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-200 shadow-md font-semibold text-lg inline-flex items-center">
        Show Map
      </button>
    </div>

    <!-- Iframe Browser Dialog -->
    <div v-if="showIframeDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <!-- Dialog Header -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
            <h3 class="text-lg font-semibold text-gray-900">Open in Browser</h3>
          </div>
          <button 
            @click="closeIframeDialog" 
            class="text-gray-400 hover:text-gray-600 transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Dialog Content -->
        <div class="mb-6">
          <p class="text-gray-700 mb-4">
            To use the location feature, please open this page in your device's default browser.
          </p>
          <p class="text-sm text-gray-600">
            Location services may not work properly when the page is loaded within another app. Opening in your browser will ensure all features work correctly.
          </p>
        </div>

        <!-- Dialog Actions -->
        <div class="flex flex-col sm:flex-row gap-3 justify-end">
          <button 
            @click="closeIframeDialog" 
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button 
            @click="openInBrowser" 
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          >
            Open in Browser
          </button>
        </div>
      </div>
    </div>

    <!-- Cashback Campaign Dialog -->
    <div v-if="showCashbackModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <!-- Dialog Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">🎁</span>
            <h3 class="text-lg font-semibold text-gray-900">Cashback Campaign</h3>
          </div>
          <button 
            @click="closeCashbackDialog" 
            class="text-gray-400 hover:text-gray-600 transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Dialog Content -->
        <div class="p-6">
          <div v-if="selectedCashbackCampaign" class="space-y-4">
            <!-- Merchant Info -->
            <div class="flex items-center space-x-3 pb-4 border-b border-gray-200">
              <img v-if="selectedMerchant?.logo" :src="selectedMerchant.logo" :alt="selectedMerchant?.name + ' Logo'" class="w-12 h-12 rounded-full object-cover">
              <div>
                <h4 class="font-semibold text-gray-900">{{ selectedMerchant?.name }}</h4>
                <p class="text-sm text-gray-600">{{ selectedMerchant?.city }}, {{ selectedMerchant?.country }}</p>
              </div>
            </div>

            <!-- Campaign Details -->
            <div class="space-y-3">
              


              <!-- Cashback Percentages -->
              <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                <div class="text-center">
                  <p class="text-lg font-semibold text-green-800 mb-2">
                    Get up to {{ Math.round(selectedCashbackCampaign.campaign.first_cashback_percentage * 100) }}% cashback! 😍
                  </p>
                  <p class="text-sm text-green-700">
                    Maximum cashback: <span class="font-semibold">{{ convertSatsToBCH(selectedCashbackCampaign.campaign.per_transaction_cashback_limit) }} BCH</span>
                    <span v-if="convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_transaction_cashback_limit)" class="text-xs text-gray-600 ml-1">
                      (≈ PHP {{ convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_transaction_cashback_limit) }})
                    </span>
                  </p>
                  <div v-if="!selectedCashbackCampaign.campaign.is_one_time_claim" class="mt-3 pt-3 border-t border-green-200">
                    <p class="text-sm text-green-700">
                      Succeeding transactions: {{ Math.round(selectedCashbackCampaign.campaign.succeeding_cashback_percentage * 100) }}% cashback
                    </p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex flex-col sm:flex-row gap-3 justify-center">
                <!-- Limits Toggle -->
                <button 
                  @click="showLimits = !showLimits" 
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-lg hover:bg-gray-200 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
                >
                  <svg v-if="!showLimits" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-if="showLimits" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  {{ showLimits ? 'Hide limits' : 'Subject to pre-defined limits' }}
                </button>

                <!-- How to Avail Button -->
                <button 
                  @click="showHowToAvail = !showHowToAvail" 
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 border border-green-600 rounded-lg hover:bg-green-700 hover:border-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200"
                >
                  <svg v-if="!showHowToAvail" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-if="showHowToAvail" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  {{ showHowToAvail ? 'Hide instructions' : 'How to avail' }}
                </button>
              </div>

              <!-- How to Avail Instructions -->
              <div v-if="showHowToAvail" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                <!-- Reserved Campaign Message -->
                <div v-if="selectedCashbackCampaign.campaign.customer_reserved_claim" class="text-center">
                  <div class="flex items-center justify-center mb-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-orange-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                    <h6 class="font-medium text-orange-900">Campaign Reserved</h6>
                  </div>
                  <div class="text-sm text-orange-800 space-y-2">
                    <p>
                      This one-time cashback promo has been reserved<span v-if="selectedCashbackCampaign.campaign.reserved_customer?.address"> for 
                      <span class="font-mono text-xs bg-orange-100 px-2 py-1 rounded">{{ truncateAddress(selectedCashbackCampaign.campaign.reserved_customer.address) }}</span></span>.
                    </p>
                    <p v-if="reservationCountdown">
                      This reservation expires in <span class="font-semibold">{{ reservationCountdown }}</span>.
                    </p>
                  </div>
                </div>

                <!-- Available Campaign Instructions -->
                <div v-else>
                  <h6 class="font-medium text-blue-900 mb-3">How to Claim Your Cashback</h6>
                  <div class="space-y-3 text-sm text-blue-800">
                    <div class="flex items-start">
                      <div class="flex-shrink-0 w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center mr-3 mt-0.5">
                        <span class="text-xs font-bold text-blue-700">1</span>
                      </div>
                      <p>
                        If the campaign is still active, cashback applies automatically after paying with BCH through Paytaca. The cashback is sent immediately after payment.
                      </p>
                    </div>
                    
                    <!-- One-time claim reservation option -->
                    <div v-if="selectedCashbackCampaign.campaign.is_one_time_claim" class="mt-4 pt-3 border-t border-blue-200">
                      <div class="flex items-start mb-3">
                        <div class="flex-shrink-0 w-6 h-6 bg-orange-200 rounded-full flex items-center justify-center mr-3 mt-0.5">
                          <span class="text-xs font-bold text-orange-700">2</span>
                        </div>
                        <p class="text-sm text-blue-800">
                          Since this is a one-time claim campaign, there is a reservation option, which will reserve the promo for you for 6 hours. You must transact within this period to claim the cashback.
                        </p>
                      </div>
                      
                      <!-- Reservation Button -->
                      <div class="ml-9">
                        <button 
                          v-if="!showReservationForm"
                          @click="showReservationForm = true" 
                          class="inline-flex items-center px-3 py-2 text-xs font-medium text-white bg-orange-600 border border-orange-600 rounded-lg hover:bg-orange-700 hover:border-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition-all duration-200"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Reserve Now
                        </button>
                        
                        <!-- Reservation Form -->
                        <div v-if="showReservationForm" class="space-y-3">
                          <div>
                            <label class="block text-xs font-medium text-blue-900 mb-1">BCH Receiving Address in Paytaca</label>
                            <input 
                              v-model="bchAddress"
                              type="text" 
                              placeholder="Enter your BCH address"
                              class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                            />
                          </div>
                          <div class="flex space-x-2">
                            <button 
                              @click="submitReservation" 
                              class="inline-flex items-center px-3 py-2 text-xs font-medium text-white bg-green-600 border border-green-600 rounded-lg hover:bg-green-700 hover:border-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200"
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                              </svg>
                              Submit Reservation
                            </button>
                            <button 
                              @click="showReservationForm = false; bchAddress = ''" 
                              class="inline-flex items-center px-3 py-2 text-xs font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-lg hover:bg-gray-200 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Limits -->
              <div v-if="showLimits" class="grid grid-cols-1 gap-3">
                <!-- Campaign Type with Explanatory Notes -->
                <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex-1">
                      <div class="text-sm font-medium text-gray-700">Campaign Type</div>
                      <div class="text-xs text-gray-600 mt-1">
                        <span v-if="selectedCashbackCampaign.campaign.is_one_time_claim">
                          This campaign can only be claimed once.
                        </span>
                        <span v-else>
                          Multiple claims are possible until any of the other set limits is reached.
                        </span>
                      </div>
                    </div>
                    <div class="text-right ml-3">
                      <span class="text-sm font-semibold" :class="selectedCashbackCampaign.campaign.is_one_time_claim ? 'text-orange-600' : 'text-green-600'">
                        {{ selectedCashbackCampaign.campaign.is_one_time_claim ? 'One-Time Claim' : 'Regular' }}
                      </span>
                    </div>
                  </div>
                  
                  <!-- Succeeding Claims Note for Regular Campaigns -->
                  <div v-if="!selectedCashbackCampaign.campaign.is_one_time_claim" class="mt-2 pt-2 border-t border-gray-200">
                    <div class="text-xs text-gray-600">
                      <span class="font-medium">Note:</span> Any succeeding claim by the same customer, the cashback percentage is reduced to 
                      <span class="font-semibold text-green-600">{{ Math.round(selectedCashbackCampaign.campaign.succeeding_cashback_percentage * 100) }}%</span>.
                    </div>
                  </div>
                </div>
                
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <div class="text-sm font-medium text-blue-800">Per Transaction Limit</div>
                      <div class="text-xs text-gray-600 mt-1">Maximum cashback you can get in a single transaction</div>
                    </div>
                    <div class="text-right ml-3">
                      <div class="text-sm font-semibold text-blue-600">{{ convertSatsToBCH(selectedCashbackCampaign.campaign.per_transaction_cashback_limit) }} BCH</div>
                      <div v-if="convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_transaction_cashback_limit)" class="text-xs text-gray-600">
                        ≈ PHP {{ convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_transaction_cashback_limit) }}
                      </div>
                    </div>
                  </div>
                </div>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <div class="text-sm font-medium text-blue-800">Per Customer Limit</div>
                      <div class="text-xs text-gray-600 mt-1">Maximum cashback you can claim in this entire campaign</div>
                    </div>
                    <div class="text-right ml-3">
                      <div class="text-sm font-semibold text-blue-600">{{ convertSatsToBCH(selectedCashbackCampaign.campaign.per_customer_cashback_limit) }} BCH</div>
                      <div v-if="convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_customer_cashback_limit)" class="text-xs text-gray-600">
                        ≈ PHP {{ convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_customer_cashback_limit) }}
                      </div>
                    </div>
                  </div>
                </div>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <div class="text-sm font-medium text-blue-800">Per Merchant Limit</div>
                      <div class="text-xs text-gray-600 mt-1">Total cashback pool for all customers in this campaign</div>
                    </div>
                    <div class="text-right ml-3">
                      <div class="text-sm font-semibold text-blue-600">{{ convertSatsToBCH(selectedCashbackCampaign.campaign.per_merchant_cashback_limit) }} BCH</div>
                      <div v-if="convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_merchant_cashback_limit)" class="text-xs text-gray-600">
                        ≈ PHP {{ convertSatsToLocalCurrency(selectedCashbackCampaign.campaign.per_merchant_cashback_limit) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Dialog Footer -->
        <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
          <button 
            @click="closeCashbackDialog" 
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-200"
          >
            Close
          </button>
          <button 
            v-if="selectedMerchant?.website_url"
            @click="visitMerchantWebsite" 
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          >
            Visit Website
          </button>
        </div>
      </div>
    </div>

  </div>

</template>

<script>
import axios from 'axios';
import MapView from '@/components/MapView.vue';
import moment from 'moment';

const DOMAIN = 'https://map.paytaca.com'

// Default map center - Philippines
const defaultCenter = [12.8797, 121.7740]; // Center of Philippines
// const defaultCenter = [11.2441900, 124.9987370]; // Tacloban City
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
      zoomLevel: 15,
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
      isFetchingMerchants: false, // Flag to prevent multiple simultaneous merchant fetches
      initialRenderComplete: false, // Add new state variable
      isGettingLocation: false, // Track location permission state
      userLocation: null, // Store user's current location
      showNearbyOnly: false, // Track if we're showing nearby merchants only
      cashbackCampaigns: [], // Store cashback campaign data
      giftObserver: null, // Intersection Observer for gift icons
      showCashbackModal: false, // Control cashback dialog visibility
      selectedCashbackCampaign: null, // Selected campaign data
      selectedMerchant: null, // Selected merchant data
      showLimits: false, // Control limits visibility in dialog
      showHowToAvail: false, // Control how to avail instructions visibility
      showReservationForm: false, // Control reservation form visibility
      bchAddress: '', // Store BCH address for reservation
      bchExchangeRate: null, // Store BCH exchange rate
      reservationCountdown: null, // Store reservation countdown
      countdownInterval: null, // Store interval for countdown timer
      pendingMapOperations: null, // Store pending map operations for mobile
      reloadTimeout: null, // Store timeout for reloading merchants when all filters are default
      showFilters: false, // Control visibility of select filter dropdowns
      showIframeDialog: false, // Control iframe browser dialog visibility
      exploreClicked: false, // Track if Explore Merchants button was clicked
      showRecentLabel: false, // Control visibility of "Recently Active Merchants" label
      recentMerchantsList: [], // Sorted list of merchants by most recent transaction
      currentRecentMerchantIndex: 0, // Current index in the recent merchants list
      highlightedMerchantId: null, // Currently highlighted merchant ID
    };
  },
  async mounted() {
    // Fetch all data in parallel for faster initial load
    this.isLoading = true;
    
    // On mobile, listen to window scroll; on desktop, listen to container scroll
    if (this.isMobile) {
      window.addEventListener('scroll', this.handleScroll);
    } else {
      this.$refs.logosContainer.addEventListener('scroll', this.handleScroll);
    }
    console.log("Scroll event listener added.");
    
    let urlParams = new URLSearchParams(window.location.search)
    if (urlParams.has('merchants')) {
      this.merchantsFilter = urlParams.get('merchants')
    }
    
    // Parse category from URL params first (need categories loaded)
    await this.fetchCategories();
    if (urlParams.has('category')) {
      const categoryShortName = urlParams.get('category')
      const category = this.categoriesList.find(cat => cat.short_name === categoryShortName)
      if (category) {
        this.filterByCategory = category.id
      }
    }
    
    // Fetch merchants and cashback campaigns in parallel
    await Promise.all([
      this.fetchMerchants(),
      this.fetchCashbackCampaigns(),
      this.fetchBCHExchangeRate()
    ]);
    
    this.setupGiftObserver(); // Setup intersection observer for gift icons
  },
      beforeUnmount() {
      // Remove scroll listener from appropriate target
      if (this.isMobile) {
        window.removeEventListener('scroll', this.handleScroll);
      } else {
        this.$refs.logosContainer.removeEventListener('scroll', this.handleScroll);
      }
      console.log("Scroll event listener removed.");
      
      // Clean up intersection observer
      if (this.giftObserver) {
        this.giftObserver.disconnect();
      }
      
      // Clean up timeout
      if (this.reloadTimeout) {
        clearTimeout(this.reloadTimeout);
      }
    },
  computed: {
    isMobile () {
      return /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) || window.innerWidth < 768
    },
    // Filtered merchants based on search query, country, category, last transaction date, and nearby location
    filteredMerchants() {
      // Don't filter if data is still loading
      if (this.isLoading || this.isFetchingMerchants) {
        return this.merchants;
      }
      
      const filtered = this.merchants.filter(merchant => {
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
    getCountryFlag(country) {
      const countryFlags = {
        'Philippines': '🇵🇭', 'PH': '🇵🇭',
        'United States': '🇺🇸', 'USA': '🇺🇸', 'US': '🇺🇸',
        'Australia': '🇦🇺', 'AU': '🇦🇺',
        'Canada': '🇨🇦', 'CA': '🇨🇦',
        'United Kingdom': '🇬🇧', 'UK': '🇬🇧', 'GB': '🇬🇧',
        'Singapore': '🇸🇬', 'SG': '🇸🇬',
        'Japan': '🇯🇵', 'JP': '🇯🇵',
        'South Korea': '🇰🇷', 'KR': '🇰🇷',
        'Thailand': '🇹🇭', 'TH': '🇹🇭',
        'Vietnam': '🇻🇳', 'VN': '🇻🇳',
        'Malaysia': '🇲🇾', 'MY': '🇲🇾',
        'Indonesia': '🇮🇩', 'ID': '🇮🇩',
        'India': '🇮🇳', 'IN': '🇮🇳',
        'Germany': '🇩🇪', 'DE': '🇩🇪',
        'France': '🇫🇷', 'FR': '🇫🇷',
        'Spain': '🇪🇸', 'ES': '🇪🇸',
        'Italy': '🇮🇹', 'IT': '🇮🇹',
        'Netherlands': '🇳🇱', 'NL': '🇳🇱',
        'Switzerland': '🇨🇭', 'CH': '🇨🇭',
        'Sweden': '🇸🇪', 'SE': '🇸🇪',
        'Norway': '🇳🇴', 'NO': '🇳🇴',
        'Denmark': '🇩🇰', 'DK': '🇩🇰',
        'Finland': '🇫🇮', 'FI': '🇫🇮',
        'Brazil': '🇧🇷', 'BR': '🇧🇷',
        'Mexico': '🇲🇽', 'MX': '🇲🇽',
        'Argentina': '🇦🇷', 'AR': '🇦🇷',
        'Chile': '🇨🇱', 'CL': '🇨🇱',
        'Colombia': '🇨🇴', 'CO': '🇨🇴',
        'South Africa': '🇿🇦', 'ZA': '🇿🇦',
        'Nigeria': '🇳🇬', 'NG': '🇳🇬',
        'Kenya': '🇰🇪', 'KE': '🇰🇪',
        'Ghana': '🇬🇭', 'GH': '🇬🇭',
        'UAE': '🇦🇪', 'United Arab Emirates': '🇦🇪',
        'Saudi Arabia': '🇸🇦', 'SA': '🇸🇦',
        'Turkey': '🇹🇷', 'TR': '🇹🇷',
        'Israel': '🇮🇱', 'IL': '🇮🇱',
        'Russia': '🇷🇺', 'RU': '🇷🇺',
        'China': '🇨🇳', 'CN': '🇨🇳',
        'Hong Kong': '🇭🇰', 'HK': '🇭🇰',
        'Taiwan': '🇹🇼', 'TW': '🇹🇼',
        'New Zealand': '🇳🇿', 'NZ': '🇳🇿',
        'Portugal': '🇵🇹', 'PT': '🇵🇹',
        'Belgium': '🇧🇪', 'BE': '🇧🇪',
        'Austria': '🇦🇹', 'AT': '🇦🇹',
        'Poland': '🇵🇱', 'PL': '🇵🇱',
        'Czech Republic': '🇨🇿', 'CZ': '🇨🇿',
        'Hungary': '🇭🇺', 'HU': '🇭🇺',
        'Greece': '🇬🇷', 'GR': '🇬🇷',
        'Ireland': '🇮🇪', 'IE': '🇮🇪',
        'Ukraine': '🇺🇦', 'UA': '🇺🇦',
        'Romania': '🇷🇴', 'RO': '🇷🇴',
        'Bulgaria': '🇧🇬', 'BG': '🇧🇬',
        'Croatia': '🇭🇷', 'HR': '🇭🇷',
        'Slovenia': '🇸🇮', 'SI': '🇸🇮',
        'Slovakia': '🇸🇰', 'SK': '🇸🇰',
        'Lithuania': '🇱🇹', 'LT': '🇱🇹',
        'Latvia': '🇱🇻', 'LV': '🇱🇻',
        'Estonia': '🇪🇪', 'EE': '🇪🇪',
        'Serbia': '🇷🇸', 'RS': '🇷🇸',
        'Montenegro': '🇲🇪', 'ME': '🇲🇪',
        'Bosnia and Herzegovina': '🇧🇦', 'BA': '🇧🇦',
        'North Macedonia': '🇲🇰', 'MK': '🇲🇰',
        'Albania': '🇦🇱', 'AL': '🇦🇱',
        'Kosovo': '🇽🇰', 'XK': '🇽🇰',
        'Moldova': '🇲🇩', 'MD': '🇲🇩',
        'Belarus': '🇧🇾', 'BY': '🇧🇾',
        'Armenia': '🇦🇲', 'AM': '🇦🇲',
        'Azerbaijan': '🇦🇿', 'AZ': '🇦🇿',
        'Georgia': '🇬🇪', 'GE': '🇬🇪',
        'Kazakhstan': '🇰🇿', 'KZ': '🇰🇿',
        'Uzbekistan': '🇺🇿', 'UZ': '🇺🇿',
        'Kyrgyzstan': '🇰🇬', 'KG': '🇰🇬',
        'Tajikistan': '🇹🇯', 'TJ': '🇹🇯',
        'Turkmenistan': '🇹🇲', 'TM': '🇹🇲',
        'Mongolia': '🇲🇳', 'MN': '🇲🇳',
        'Nepal': '🇳🇵', 'NP': '🇳🇵',
        'Bangladesh': '🇧🇩', 'BD': '🇧🇩',
        'Sri Lanka': '🇱🇰', 'LK': '🇱🇰',
        'Pakistan': '🇵🇰', 'PK': '🇵🇰',
        'Afghanistan': '🇦🇫', 'AF': '🇦🇫',
        'Iran': '🇮🇷', 'IR': '🇮🇷',
        'Iraq': '🇮🇶', 'IQ': '🇮🇶',
        'Syria': '🇸🇾', 'SY': '🇸🇾',
        'Lebanon': '🇱🇧', 'LB': '🇱🇧',
        'Jordan': '🇯🇴', 'JO': '🇯🇴',
        'Kuwait': '🇰🇼', 'KW': '🇰🇼',
        'Bahrain': '🇧🇭', 'BH': '🇧🇭',
        'Qatar': '🇶🇦', 'QA': '🇶🇦',
        'Oman': '🇴🇲', 'OM': '🇴🇲',
        'Yemen': '🇾🇪', 'YE': '🇾🇪',
        'Egypt': '🇪🇬', 'EG': '🇪🇬',
        'Libya': '🇱🇾', 'LY': '🇱🇾',
        'Tunisia': '🇹🇳', 'TN': '🇹🇳',
        'Algeria': '🇩🇿', 'DZ': '🇩🇿',
        'Morocco': '🇲🇦', 'MA': '🇲🇦',
        'Sudan': '🇸🇩', 'SD': '🇸🇩',
        'Ethiopia': '🇪🇹', 'ET': '🇪🇹',
        'Somalia': '🇸🇴', 'SO': '🇸🇴',
        'Djibouti': '🇩🇯', 'DJ': '🇩🇯',
        'Eritrea': '🇪🇷', 'ER': '🇪🇷',
        'Uganda': '🇺🇬', 'UG': '🇺🇬',
        'Rwanda': '🇷🇼', 'RW': '🇷🇼',
        'Burundi': '🇧🇮', 'BI': '🇧🇮',
        'Tanzania': '🇹🇿', 'TZ': '🇹🇿',
        'Zambia': '🇿🇲', 'ZM': '🇿🇲',
        'Zimbabwe': '🇿🇼', 'ZW': '🇿🇼',
        'Malawi': '🇲🇼', 'MW': '🇲🇼',
        'Mozambique': '🇲🇿', 'MZ': '🇲🇿',
        'Madagascar': '🇲🇬', 'MG': '🇲🇬',
        'Mauritius': '🇲🇺', 'MU': '🇲🇺',
        'Seychelles': '🇸🇨', 'SC': '🇸🇨',
        'Comoros': '🇰🇲', 'KM': '🇰🇲',
        'Botswana': '🇧🇼', 'BW': '🇧🇼',
        'Namibia': '🇳🇦', 'NA': '🇳🇦',
        'Angola': '🇦🇴', 'AO': '🇦🇴',
        'Democratic Republic of the Congo': '🇨🇩', 'DR Congo': '🇨🇩', 'DRC': '🇨🇩', 'CD': '🇨🇩',
        'Republic of the Congo': '🇨🇬', 'Congo': '🇨🇬', 'CG': '🇨🇬',
        'Gabon': '🇬🇦', 'GA': '🇬🇦',
        'Equatorial Guinea': '🇬🇶', 'GQ': '🇬🇶',
        'Cameroon': '🇨🇲', 'CM': '🇨🇲',
        'Central African Republic': '🇨🇫', 'CF': '🇨🇫',
        'Chad': '🇹🇩', 'TD': '🇹🇩',
        'Niger': '🇳🇪', 'NE': '🇳🇪',
        'Mali': '🇲🇱', 'ML': '🇲🇱',
        'Burkina Faso': '🇧🇫', 'BF': '🇧🇫',
        'Senegal': '🇸🇳', 'SN': '🇸🇳',
        'Gambia': '🇬🇲', 'GM': '🇬🇲',
        'Guinea-Bissau': '🇬🇼', 'GW': '🇬🇼',
        'Guinea': '🇬🇳', 'GN': '🇬🇳',
        'Sierra Leone': '🇸🇱', 'SL': '🇸🇱',
        'Liberia': '🇱🇷', 'LR': '🇱🇷',
        'Ivory Coast': '🇨🇮', "Côte d'Ivoire": '🇨🇮', 'CI': '🇨🇮',
        'Togo': '🇹🇬', 'TG': '🇹🇬',
        'Benin': '🇧🇯', 'BJ': '🇧🇯',
        'Mauritania': '🇲🇷', 'MR': '🇲🇷',
        'Cape Verde': '🇨🇻', 'Cabo Verde': '🇨🇻', 'CV': '🇨🇻',
        'Sao Tome and Principe': '🇸🇹', 'ST': '🇸🇹',
        'Lesotho': '🇱🇸', 'LS': '🇱🇸',
        'Eswatini': '🇸🇿', 'Swaziland': '🇸🇿', 'SZ': '🇸🇿',
        'Peru': '🇵🇪', 'PE': '🇵🇪',
        'Bolivia': '🇧🇴', 'BO': '🇧🇴',
        'Paraguay': '🇵🇾', 'PY': '🇵🇾',
        'Uruguay': '🇺🇾', 'UY': '🇺🇾',
        'Ecuador': '🇪🇨', 'EC': '🇪🇨',
        'Venezuela': '🇻🇪', 'VE': '🇻🇪',
        'Guyana': '🇬🇾', 'GY': '🇬🇾',
        'Suriname': '🇸🇷', 'SR': '🇸🇷',
        'French Guiana': '🇬🇫', 'GF': '🇬🇫',
        'Belize': '🇧🇿', 'BZ': '🇧🇿',
        'Guatemala': '🇬🇹', 'GT': '🇬🇹',
        'Honduras': '🇭🇳', 'HN': '🇭🇳',
        'El Salvador': '🇸🇻', 'SV': '🇸🇻',
        'Nicaragua': '🇳🇮', 'NI': '🇳🇮',
        'Costa Rica': '🇨🇷', 'CR': '🇨🇷',
        'Panama': '🇵🇦', 'PA': '🇵🇦',
        'Cuba': '🇨🇺', 'CU': '🇨🇺',
        'Jamaica': '🇯🇲', 'JM': '🇯🇲',
        'Haiti': '🇭🇹', 'HT': '🇭🇹',
        'Dominican Republic': '🇩🇴', 'DO': '🇩🇴',
        'Puerto Rico': '🇵🇷', 'PR': '🇵🇷',
        'Trinidad and Tobago': '🇹🇹', 'TT': '🇹🇹',
        'Barbados': '🇧🇧', 'BB': '🇧🇧',
        'Saint Lucia': '🇱🇨', 'LC': '🇱🇨',
        'Grenada': '🇬🇩', 'GD': '🇬🇩',
        'Saint Vincent and the Grenadines': '🇻🇨', 'VC': '🇻🇨',
        'Antigua and Barbuda': '🇦🇬', 'AG': '🇦🇬',
        'Dominica': '🇩🇲', 'DM': '🇩🇲',
        'Saint Kitts and Nevis': '🇰🇳', 'KN': '🇰🇳',
        'Bahamas': '🇧🇸', 'BS': '🇧🇸',
        'Cayman Islands': '🇰🇾', 'KY': '🇰🇾',
        'Bermuda': '🇧🇲', 'BM': '🇧🇲',
        'Aruba': '🇦🇼', 'AW': '🇦🇼',
        'Curacao': '🇨🇼', 'CW': '🇨🇼',
        'Sint Maarten': '🇸🇽', 'SX': '🇸🇽',
        'US Virgin Islands': '🇻🇮', 'VI': '🇻🇮',
        'British Virgin Islands': '🇻🇬', 'VG': '🇻🇬',
        'Anguilla': '🇦🇮', 'AI': '🇦🇮',
        'Montserrat': '🇲🇸', 'MS': '🇲🇸',
        'Guadeloupe': '🇬🇵', 'GP': '🇬🇵',
        'Martinique': '🇲🇶', 'MQ': '🇲🇶',
        'Saint Barthelemy': '🇧🇱', 'BL': '🇧🇱',
        'Saint Martin': '🇲🇫', 'MF': '🇲🇫',
        'Sint Eustatius': '🇧🇶', 'BQ': '🇧🇶',
        'Saba': '🇧🇶',
        'Saint Pierre and Miquelon': '🇵🇲', 'PM': '🇵🇲',
        'Greenland': '🇬🇱', 'GL': '🇬🇱',
        'Falkland Islands': '🇫🇰', 'FK': '🇫🇰',
        'South Georgia and the South Sandwich Islands': '🇬🇸', 'GS': '🇬🇸',
        'Antarctica': '🇦🇶', 'AQ': '🇦🇶'
      };
      return countryFlags[country] || '🏳️';
    },
    fetchMerchants() {
      // Prevent multiple simultaneous API calls
      if (this.isFetchingMerchants) {
        return;
      }
      
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
      
      this.isFetchingMerchants = true; // Set flag to prevent multiple calls
      this.isLoading = true; // Set loading state to true before API call
      return axios.get(url)
        .then(response => {
          // The API already returns location and logo fields directly on merchant objects
          // Map logo_url to logo for consistency with existing template code
          const merchants = response.data.map(merchant => ({
            ...merchant,
            logo: merchant.logo_url || null
          }));
          
          // Ensure merchants are unique by ID to prevent duplicates
          this.merchants = this.deduplicateMerchants(merchants);
          this.isLoading = false;
          this.isFetchingMerchants = false; // Reset flag when loading is complete
          // Use nextTick to ensure DOM is updated before showing the button
          this.$nextTick(() => {
            setTimeout(() => {
              this.initialRenderComplete = true;
              // Observe gift icons after initial render
              this.observeGiftIcons();
            }, 100); // Small delay to ensure smooth transition
          });
        })
        .catch(error => {
          console.error('Error fetching merchants:', error);
          this.isLoading = false; // Set loading state to false on error
          this.isFetchingMerchants = false; // Reset flag on error
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
    fetchCashbackCampaigns() {
      return axios.get('https://engagementhub.paytaca.com/api/cashback/campaignmerchant/get_merchants_under_campaigns/')
        .then(response => {
          this.cashbackCampaigns = response.data;
        })
        .catch(error => {
          console.error('Error fetching cashback campaigns:', error);
          this.cashbackCampaigns = []; // Set empty array on error
        });
    },
    getGoogleMapLink(merchant) {
      if (merchant.gmap_business_link) {
        return merchant.gmap_business_link
      } else {
        return `https://www.google.com/maps?q=${merchant.latitude},${merchant.longitude}`
      }
    },
    showPopup(merchant, skipToggle = false) {

      this.zoomLevel = 17.5
      
      if (this.isMobile && !skipToggle) {
        // Store merchant data for delayed execution
        this.pendingMapOperations = merchant;
        this.toggleMapView();
        return; // Exit early for mobile
      }

      // For desktop, perform map operations immediately
      this.performMapOperations(merchant);
    },

    // Helper method to perform map operations
    performMapOperations(merchant) {
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

      const countryFlag = this.getCountryFlag(merchant.country);

      let popupContent = `<div class="rounded-lg"><div class="flex items-center justify-between"><h3 class='text-lg font-semibold text-gray-900'>${merchant.name}</h3>`;
      
      // Include merchant logo if available
      if (merchant.logo) {
        popupContent += `<img src="${merchant.logo}" alt="${merchant.name} Logo" class="h-16 w-16 rounded-full">`;
      }
      
      popupContent += `</div><div>`;
      
      // Include merchant information if available
      if (merchant.city) {
        popupContent += `<div class="flex items-center justify-between"><p>${merchant.city}, ${merchant.country}</p><span class="text-2xl ml-2">${countryFlag}</span></div>`;
      } else if (merchant.town) {
        popupContent += `<div class="flex items-center justify-between"><p>${merchant.town}, ${merchant.province}, ${merchant.country}</p><span class="text-2xl ml-2">${countryFlag}</span></div>`;
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
      if (this.isMobile) {
        // Mobile: use window scroll
        const scrollPosition = window.scrollY + window.innerHeight;
        const scrollHeight = document.documentElement.scrollHeight - 100;
        
        if (scrollPosition >= scrollHeight) {
          console.log("Reached bottom of page. Loading more merchants...");
          this.loadMoreMerchants();
        }
      } else {
        // Desktop: use container scroll
        const container = this.$refs.logosContainer;
        const scrollPosition = container.scrollTop + container.clientHeight;
        const scrollHeight = container.scrollHeight - 100;
        
        if (scrollPosition >= scrollHeight) {
          console.log("Reached bottom of container. Loading more merchants...");
          this.loadMoreMerchants();
        }
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

      if (this.isMobile && this.currentView === 'map' && !this.pendingMapOperations) {
        // When switching to map view on mobile (without pending merchant), fit the viewport properly
        this.$nextTick(() => {
          this.$refs.mapView.fitViewportWhenVisible();
        });
      }
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
      if (!dateString) return 'N/A';
      
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
    
    // Format date for display (not relative time)
    formatDisplayDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
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
    
    // Check if page is loaded in an iframe
    isInIframe() {
      try {
        return window.self !== window.top;
      } catch (e) {
        return true;
      }
    },
    
    // Show merchants within 10km of user location
    showMerchantsNearMe() {
      // Check if we're in an iframe
      if (this.isInIframe()) {
        this.showIframeDialog = true;
        return;
      }
      
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
    
    // Open page in default browser
    openInBrowser() {
      const currentUrl = window.location.href;
      // Try to open in a new window/tab
      window.open(currentUrl, '_blank');
      this.showIframeDialog = false;
    },
    
    // Close iframe dialog
    closeIframeDialog() {
      this.showIframeDialog = false;
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
    },

    // Check if a merchant has a cashback campaign
    hasCashbackCampaign(merchant) {
      if (!merchant.watchtower_merchant_id) return false;
      return this.cashbackCampaigns.some(campaign => {
        // Check if merchant ID matches
        if (campaign.merchant_id !== merchant.watchtower_merchant_id) return false;
        
        // For one-time claim campaigns, check if it hasn't been claimed
        if (campaign.campaign.is_one_time_claim) {
          return !campaign.campaign.has_been_claimed;
        }
        
        // For regular campaigns, check if end period hasn't expired
        if (campaign.campaign.end_period) {
          const endDate = new Date(campaign.campaign.end_period);
          const currentDate = new Date();
          return endDate > currentDate;
        }
        
        // If no end period, campaign is considered active
        return true;
      });
    },
    
    // Setup intersection observer for gift icons
    setupGiftObserver() {
      if (!window.IntersectionObserver) {
        console.warn('IntersectionObserver not supported');
        return;
      }
      
      this.giftObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // Add animation class when gift icon comes into view
            entry.target.classList.add('animate-gift');
          } else {
            // Remove animation class when gift icon goes out of view
            entry.target.classList.remove('animate-gift');
          }
        });
      }, {
        threshold: 0.3, // Trigger when 30% of the element is visible
        rootMargin: '50px' // Start animation slightly before the element comes into view
      });
      
      // Observe all gift icons after the next DOM update
      this.$nextTick(() => {
        this.observeGiftIcons();
      });
    },
    
    // Observe all gift icons
    observeGiftIcons() {
      const giftIcons = document.querySelectorAll('.gift-icon');
      giftIcons.forEach(icon => {
        this.giftObserver.observe(icon);
      });
    },
    
    // Show cashback campaign dialog
    showCashbackDialog(merchant) {
      const campaign = this.cashbackCampaigns.find(c => c.merchant_id === merchant.watchtower_merchant_id);
      if (campaign) {
        this.selectedCashbackCampaign = campaign;
        this.selectedMerchant = merchant;
        this.showCashbackModal = true;
        this.showLimits = false; // Reset limits visibility
        this.showHowToAvail = false; // Reset how to avail visibility
        this.showReservationForm = false; // Reset reservation form visibility
        this.bchAddress = ''; // Reset BCH address
        
        // Start countdown if campaign is reserved
        if (campaign.campaign.customer_reserved_claim && campaign.campaign.reserved_customer?.date_reserved) {
          this.startReservationCountdown(campaign.campaign.reserved_customer.date_reserved);
        }
        
        // Prevent body scroll when modal is open
        document.body.style.overflow = 'hidden';
      }
    },
    
    // Close cashback campaign dialog
    closeCashbackDialog() {
      this.showCashbackModal = false;
      this.selectedCashbackCampaign = null;
      this.selectedMerchant = null;
      this.showLimits = false; // Reset limits visibility
      this.showHowToAvail = false; // Reset how to avail visibility
      this.showReservationForm = false; // Reset reservation form visibility
      this.bchAddress = ''; // Reset BCH address
      
      // Clear countdown timer
      this.clearReservationCountdown();
      
      // Restore body scroll
      document.body.style.overflow = 'auto';
    },
    
    // Visit merchant website from dialog
    visitMerchantWebsite() {
      if (this.selectedMerchant?.website_url) {
        window.open(this.selectedMerchant.website_url, '_blank');
      }
    },
    
    // Submit reservation for one-time claim campaign
    async submitReservation() {
      if (!this.bchAddress.trim()) {
        alert('Please enter your BCH receiving address');
        return;
      }
      
      try {
        const payload = {
          merchant_id: this.selectedMerchant.watchtower_merchant_id,
          customer_address: this.bchAddress.trim()
        };
        
        console.log('Submitting reservation:', payload);
        
        const response = await axios.post('https://engagementhub.paytaca.com/api/cashback/customerclaim/', payload);
        
        console.log('Reservation response:', response.data);
        
        // Show success message
        alert('Reservation submitted successfully! The promo is reserved for you for 6 hours.');
        
        // Reset form
        this.showReservationForm = false;
        this.bchAddress = '';
        
      } catch (error) {
        console.error('Error submitting reservation:', error);
        
        // Show error message
        if (error.response && error.response.data) {
          alert(`Reservation failed: ${error.response.data.message || 'Unknown error occurred'}`);
        } else {
          alert('Reservation failed. Please try again later.');
        }
      }
    },
    
    // Fetch BCH exchange rate
    async fetchBCHExchangeRate() {
      try {
        const response = await axios.get('https://watchtower.cash/api/bch-prices/?currencies=PHP');
        if (response.data && response.data.length > 0) {
          this.bchExchangeRate = parseFloat(response.data[0].price_value);
        }
      } catch (error) {
        this.bchExchangeRate = null;
      }
    },
    
    // Convert satoshis to BCH
    convertSatsToBCH(sats) {
      if (!sats) return null;
      
      // 1 BCH = 100,000,000 satoshis
      const bchAmount = sats / 100000000;
      
      return bchAmount.toFixed(8);
    },
    
    // Start reservation countdown timer
    startReservationCountdown(dateReserved) {
      this.clearReservationCountdown(); // Clear any existing timer
      
      const updateCountdown = () => {
        const reservedDate = new Date(dateReserved);
        const expirationDate = new Date(reservedDate.getTime() + (6 * 60 * 60 * 1000)); // Add 6 hours
        const currentDate = new Date();
        const timeDifference = expirationDate - currentDate;
        
        if (timeDifference <= 0) {
          this.reservationCountdown = 'Expired';
          this.clearReservationCountdown();
          return;
        }
        
        const hours = Math.floor(timeDifference / (1000 * 60 * 60));
        const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
        
        this.reservationCountdown = `${hours}h ${minutes}m ${seconds}s`;
      };
      
      // Update immediately
      updateCountdown();
      
      // Update every second
      this.countdownInterval = setInterval(updateCountdown, 1000);
    },
    
    // Clear reservation countdown timer
    clearReservationCountdown() {
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
      }
      this.reservationCountdown = null;
    },
    
    // Truncate BCH address for display
    truncateAddress(address) {
      if (!address) return '';
      if (address.length <= 15) return address;
      
      const prefix = address.substring(0, 16); // "bitcoincash:"
      const suffix = address.substring(address.length - 4); // last 4 characters
      return `${prefix}...${suffix}`;
    },
    
    // Convert satoshis to local currency
    convertSatsToLocalCurrency(sats) {
      if (!this.bchExchangeRate || !sats) return null;
      
      // 1 BCH = 100,000,000 satoshis
      const bchAmount = sats / 100000000;
      const localAmount = bchAmount * this.bchExchangeRate;
      
      return localAmount.toFixed(2);
    },
    
    // Deduplicate merchants by ID to prevent duplicates
    deduplicateMerchants(merchants) {
      const seen = new Set();
      return merchants.filter(merchant => {
        if (seen.has(merchant.id)) {
          return false;
        }
        seen.add(merchant.id);
        return true;
      });
    },
    
    // Check if all filters are at default values and reload merchants if so
    checkAndReloadIfAllFiltersDefault() {
      // Add a small delay to prevent multiple API calls when multiple filters change
      clearTimeout(this.reloadTimeout);
      this.reloadTimeout = setTimeout(() => {
        const allFiltersDefault = 
          this.filterByCountry === 'default' &&
          this.filterByCity === 'default' &&
          this.filterByCategory === 'default' &&
          this.filterByLastTransaction === 'default' &&
          !this.showUnverified &&
          !this.showNearbyOnly &&
          !this.searchQuery;
        
        if (allFiltersDefault && !this.isFetchingMerchants) {
          this.fetchMerchants();
        }
      }, 100);
    },

    // Reset explore mode to initial state
    resetExploreMode() {
      this.exploreClicked = false;
      this.showRecentLabel = false;
      this.recentMerchantsList = [];
      this.currentRecentMerchantIndex = 0;
      this.highlightedMerchantId = null;
    },

    // Handle Explore Merchants button click
    exploreRecentMerchants() {
      // Fade out button by setting exploreClicked to true
      this.exploreClicked = true;
      
      // Build and sort the list of recent merchants
      this.buildRecentMerchantsList();
      
      // Show the label after a short delay
      setTimeout(() => {
        this.showRecentLabel = true;
      }, 300);
      
      // Get the first merchant (most recent)
      if (this.recentMerchantsList.length > 0) {
        this.currentRecentMerchantIndex = 0;
        const mostRecentMerchant = this.recentMerchantsList[0];
        
        // On mobile, switch to map view first
        if (this.isMobile) {
          this.currentView = 'map';
          // Wait for map to be ready, then focus
          this.$nextTick(() => {
            setTimeout(() => {
              this.focusOnMerchant(mostRecentMerchant);
            }, 300);
          });
        } else {
          // On desktop, wait for the button fade animation, then zoom
          setTimeout(() => {
            this.focusOnMerchant(mostRecentMerchant);
          }, 600);
        }
      }
    },

    // Build the sorted list of merchants with recent transactions
    buildRecentMerchantsList() {
      if (!this.filteredMerchants || this.filteredMerchants.length === 0) {
        this.recentMerchantsList = [];
        return;
      }

      // Filter merchants that have a last_transaction_date and sort them
      this.recentMerchantsList = this.filteredMerchants
        .filter(merchant => merchant.last_transaction_date)
        .sort((a, b) => {
          const dateA = new Date(a.last_transaction_date);
          const dateB = new Date(b.last_transaction_date);
          return dateB - dateA; // Descending order (most recent first)
        });
    },

    // Go to the next recent merchant in the list
    goToNextRecentMerchant() {
      if (this.recentMerchantsList.length === 0) {
        this.buildRecentMerchantsList();
      }

      if (this.recentMerchantsList.length === 0) {
        return; // No merchants with transactions
      }

      // Move to the next index, wrap around if at the end
      this.currentRecentMerchantIndex = (this.currentRecentMerchantIndex + 1) % this.recentMerchantsList.length;
      
      const nextMerchant = this.recentMerchantsList[this.currentRecentMerchantIndex];
      
      // On mobile, ensure we're in map view
      if (this.isMobile) {
        this.currentView = 'map';
      }
      
      // Focus on the merchant (zoom, highlight, scroll)
      this.focusOnMerchant(nextMerchant);
    },

    // Focus on a merchant: zoom to it, highlight it, show popup, and scroll to it in the list (desktop only)
    focusOnMerchant(merchant) {
      if (!merchant) return;

      // On desktop, set the highlighted merchant ID and scroll to card
      // On mobile, skip highlighting since we're in map view
      if (!this.isMobile) {
        this.highlightedMerchantId = merchant.id;
        this.scrollToMerchantCard(merchant.id);
      }
      
      // Zoom to the merchant on the map and show popup after zoom completes
      this.zoomToMerchant(merchant, () => {
        // Wait 500ms after zoom completes, then show the popup
        setTimeout(() => {
          // On mobile, skip the view toggle since we're already in map view
          this.showPopup(merchant, this.isMobile);
        }, 500);
      });
    },

    // Scroll to the merchant card in the list and center it vertically
    scrollToMerchantCard(merchantId) {
      this.$nextTick(() => {
        const merchantCard = document.querySelector(`[data-merchant-id="${merchantId}"]`);
        if (merchantCard && this.$refs.logosContainer) {
          // Calculate the position to scroll to
          const container = this.$refs.logosContainer;
          const cardTop = merchantCard.offsetTop;
          const cardHeight = merchantCard.offsetHeight;
          const containerHeight = container.clientHeight;
          
          // Calculate the scroll position to center the card vertically
          const scrollPosition = cardTop - (containerHeight / 2) + (cardHeight / 2);
          
          // Scroll the container to center the card
          container.scrollTo({
            top: Math.max(0, scrollPosition),
            behavior: 'smooth'
          });
        }
      });
    },

    // Zoom to a specific merchant on the map
    zoomToMerchant(merchant, onComplete) {
      if (this.$refs.mapView && merchant && merchant.latitude && merchant.longitude) {
        const zoomLevel = 16; // Close zoom level to see the merchant clearly
        this.$refs.mapView.centerOnTarget([merchant.latitude, merchant.longitude], zoomLevel, onComplete);
      }
    },
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
        
        // Reset explore mode when search changes
        this.resetExploreMode();
      }
    },
    filterByCountry(newValue) {
      if (newValue !== 'default') {
        // For any country selection, use default values and let MapView auto-fit to markers
        this.mapCenter = defaultCenter;
        this.zoomLevel = 4;
        
        // Reset city filter when country changes
        this.filterByCity = 'default';
        
        // Only update map if map view is currently active
        if (this.currentView === 'map' && !this.isMobile) {
          this.$refs.mapView.centerOnTarget(this.mapCenter, this.zoomLevel);
        }
      } else {
        this.mapCenter = defaultCenter;
        this.zoomLevel = 4;
        
        // Reset city filter when country is reset to default
        this.filterByCity = 'default';
        
        // Only update map if map view is currently active
        if (this.currentView === 'map' && !this.isMobile) {
          this.$refs.mapView.centerOnTarget(this.mapCenter, this.zoomLevel);
        }
      }
      
      // Check if all filters are now default and reload if so
      this.checkAndReloadIfAllFiltersDefault();
    },
    filterByCity(newValue) {
      if (newValue !== 'default') {
        // For any city selection, use default values and let MapView auto-fit to markers
        this.mapCenter = defaultCenter;
        this.zoomLevel = 4;
        
        // Only update map if map view is currently active
        if (this.currentView === 'map' && !this.isMobile) {
          this.$refs.mapView.centerOnTarget(this.mapCenter, this.zoomLevel);
        }
      }
      
      // Check if all filters are now default and reload if so
      this.checkAndReloadIfAllFiltersDefault();
    },
    
    // Watch for other filter changes
    filterByCategory(newValue, oldValue) {
      // Only fetch if the value actually changed and is not being reset
      if (newValue !== oldValue && newValue !== 'default') {
        this.fetchMerchants();
      } else if (newValue === 'default') {
        // Check if all filters are now default and reload if so
        this.checkAndReloadIfAllFiltersDefault();
      }
    },
    filterByLastTransaction(newValue, oldValue) {
      // Only fetch if the value actually changed and is not being reset
      if (newValue !== oldValue && newValue !== 'default') {
        this.fetchMerchants();
      } else if (newValue === 'default') {
        // Check if all filters are now default and reload if so
        this.checkAndReloadIfAllFiltersDefault();
      }
    },
    showUnverified() {
      this.checkAndReloadIfAllFiltersDefault();
    },
    showNearbyOnly() {
      this.checkAndReloadIfAllFiltersDefault();
    },
    
    // Watch for changes in filtered merchants to observe new gift icons
    filteredMerchants: {
      handler() {
        this.$nextTick(() => {
          this.observeGiftIcons();
        });
        
        // If we're in explore mode, rebuild the recent merchants list
        if (this.exploreClicked) {
          this.buildRecentMerchantsList();
        }
      },
      deep: true
    },
    
    
    // Watch for view changes to handle pending map operations on mobile
    currentView(newView, oldView) {
      if (this.isMobile && newView === 'map' && oldView === 'list' && this.pendingMapOperations) {
        // Wait for map to be ready, then execute pending operations
        this.$nextTick(() => {
          setTimeout(() => {
            if (this.$refs.mapView && this.$refs.mapView.map) {
              this.performMapOperations(this.pendingMapOperations);
              this.pendingMapOperations = null; // Clear pending operations
            }
          }, 150); // Give map time to be fully ready after invalidateSize
        });
      }
    }
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

/* Gift icon animations */
.gift-icon {
  transition: all 0.3s ease;
  filter: drop-shadow(0 0 0 rgba(255, 193, 7, 0));
}

.gift-icon.animate-gift {
  animation: giftUnpack 2s ease-in-out infinite;
}

@keyframes giftUnpack {
  0% {
    transform: scale(1) rotate(0deg);
    filter: drop-shadow(0 0 0 rgba(255, 193, 7, 0));
  }
  25% {
    transform: scale(1.2) rotate(-5deg);
    filter: drop-shadow(0 0 8px rgba(255, 193, 7, 0.8));
  }
  50% {
    transform: scale(1.1) rotate(5deg);
    filter: drop-shadow(0 0 12px rgba(255, 193, 7, 1));
  }
  75% {
    transform: scale(1.2) rotate(-3deg);
    filter: drop-shadow(0 0 8px rgba(255, 193, 7, 0.8));
  }
  100% {
    transform: scale(1) rotate(0deg);
    filter: drop-shadow(0 0 0 rgba(255, 193, 7, 0));
  }
}

/* Pulsing glow effect */
.gift-icon.animate-gift::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 193, 7, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: giftGlow 2s ease-in-out infinite;
  pointer-events: none;
  z-index: -1;
}

@keyframes giftGlow {
  0%, 100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.5);
  }
}

/* Highlighted merchant card styles */
[data-merchant-id].ring-4 {
  animation: highlight-pulse 2s ease-in-out infinite;
}

@keyframes highlight-pulse {
  0%, 100% {
    box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.5), 0 10px 25px -5px rgba(59, 130, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(96, 165, 250, 0.3), 0 10px 25px -5px rgba(59, 130, 246, 0.5);
  }
}

/* Current badge animation */
.absolute.bg-blue-600 {
  animation: badge-bounce 0.5s ease-out;
}

@keyframes badge-bounce {
  0% {
    transform: scale(0) translateY(10px);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) translateY(-2px);
  }
  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

</style>
