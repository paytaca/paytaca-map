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
      <div v-if="!isLoading && !isFetchingMerchants" class="text-center mb-6">
        <p class="text-white text-lg font-medium">{{ filteredMerchants.length }} merchants</p>
        <p v-if="showNearbyOnly && userLocation" class="text-green-400 text-sm mt-1">
          📍 Showing merchants within 10km of your location
        </p>
      </div>

      <!-- Grid for logos with descriptions -->
      <div v-if="!isLoading" class="mt-2 grid grid-cols-1 md:grid-cols-2 w-85 md-270 lg-255 h-auto md-auto">
        <!-- Logos with descriptions -->
        <div v-for="merchant in paginatedMerchants" :key="merchant.id" 
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
              <span v-if="hasCashbackCampaign(merchant)" 
                    class="gift-icon inline-flex items-center text-yellow-400 animate-gift cursor-pointer" 
                    title="Click to view cashback details"
                    :ref="`gift-${merchant.id}`"
                    @click.stop="showCashbackDialog(merchant)">🎁</span>
            </p>
        </div>
      </div>

      <!-- Loading Spinner -->
      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
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
      reloadTimeout: null // Store timeout for reloading merchants when all filters are default
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
    await this.fetchCashbackCampaigns(); // Fetch cashback campaigns on component mount
    await this.fetchBCHExchangeRate(); // Fetch BCH exchange rate
    this.setupGiftObserver(); // Setup intersection observer for gift icons
  },
      beforeUnmount() {
      this.$refs.logosContainer.removeEventListener('scroll', this.handleScroll);
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
      axios.get(url)
        .then(response => {
          const merchants = response.data;
          this.fetchLocations(merchants);
        })
        .catch(error => {
          console.error('Error fetching merchants:', error);
          this.isLoading = false; // Set loading state to false on error
          this.isFetchingMerchants = false; // Reset flag on error
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
          
          // Create new merchant objects instead of mutating existing ones
          const merchantsWithLocations = merchants.map(merchant => {
            const location = locationMap.get(merchant.id);
            if (location) {
              return {
                ...merchant,
                location: location.location,
                town: location.town,
                city: location.city,
                province: location.province,
                state: location.state,
                country: location.country,
                latitude: location.latitude,
                longitude: location.longitude
              };
            }
            return merchant;
          });
          
          this.merchants = merchantsWithLocations;
          this.fetchLogos();
        })
        .catch(error => {
          console.error('Error fetching locations:', error);
          this.isLoading = false; // Set loading state to false on error
          this.isFetchingMerchants = false; // Reset flag on error
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
          
          // Create new merchant objects instead of mutating existing ones
          const merchantsWithLogos = this.merchants.map(merchant => {
            const logos = logoMap.get(merchant.id);
            return {
              ...merchant,
              logo: logos ? logos[0] : null
            };
          });
          
          // Ensure merchants are unique by ID to prevent duplicates
          const deduplicatedMerchants = this.deduplicateMerchants(merchantsWithLogos);
          this.merchants = deduplicatedMerchants;
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
          console.error('Error fetching logos:', error);
          this.isLoading = false;
          this.isFetchingMerchants = false; // Reset flag on error
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
    showPopup(merchant) {

      this.zoomLevel = 17.5
      
      if (this.isMobile) {
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
      
      // Check if all filters are now default and reload if so
      this.checkAndReloadIfAllFiltersDefault();
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
      },
      deep: true
    },
    
    
    // Watch for view changes to handle pending map operations on mobile
    currentView(newView, oldView) {
      if (this.isMobile && newView === 'map' && oldView === 'list' && this.pendingMapOperations) {
        // Wait for map to be ready, then execute pending operations
        this.$nextTick(() => {
          setTimeout(() => {
            if (this.$refs.mapView && this.$refs.mapView.centerOnTarget) {
              this.performMapOperations(this.pendingMapOperations);
              this.pendingMapOperations = null; // Clear pending operations
            }
          }, 300); // Give map more time to be fully ready
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

</style>
