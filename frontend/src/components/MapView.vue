<template>
  <div class="map-container w-full h-screen">
    <div ref="map" class="w-full h-full"></div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet.markercluster/dist/leaflet.markercluster';
import image from "../assets/marker_pin.png";


// Default map center - Philippines
const defaultCenter = [12.8797, 121.7740]; // Center of Philippines
// const defaultCenter = [11.2441900, 124.9987370]; // Tacloban City
// const defaultCenter = [-2.745453205711577, 129.97266776311113]; // Custom

export default {
  name: 'MapView',
  props: {
    merchants: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      initialLoadComplete: false,
      isInitialDataLoad: true,
    };
  },
  mounted () {
    this.loadMap();
    // After 3 seconds, consider initial data load complete
    setTimeout(() => {
      this.isInitialDataLoad = false;
    }, 3000);
  },
  watch: {
    merchants: {
      handler(newMerchants) {
        this.updateMarkers(newMerchants);
      },
      deep: true,
    },
  },
  methods: {
    loadMap() {
      // Initialize map without setting a specific view initially
      this.map = L.map(this.$refs.map);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);

      // Initialize marker cluster group with dense clustering effect
      this.markerClusterGroup = L.markerClusterGroup({
        maxClusterRadius: 15,
        chunkedLoading: true,
        animate: true,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        spiderfyDistanceMultiplier: 1.5,  // Spread pins further apart when spiderfying
        iconCreateFunction: function(cluster) {
          const childCount = cluster.getChildCount();
          let size = 40;
          let fontSize = 14;
          let backgroundColor = 'rgba(34, 197, 94, 0.7)'; // green-500 with transparency
          let borderColor = '#16a34a';
          
          // Scale cluster size and color based on count
          if (childCount < 10) {
            size = 40;
            fontSize = 14;
          } else if (childCount < 50) {
            size = 50;
            fontSize = 16;
            backgroundColor = 'rgba(59, 130, 246, 0.75)'; // blue-500 with transparency
            borderColor = '#2563eb';
          } else if (childCount < 100) {
            size = 60;
            fontSize = 18;
            backgroundColor = 'rgba(147, 51, 234, 0.75)'; // purple-500 with transparency
            borderColor = '#7c3aed';
          } else {
            size = 70;
            fontSize = 20;
            backgroundColor = 'rgba(239, 68, 68, 0.75)'; // red-500 with transparency
            borderColor = '#dc2626';
          }
          
          return L.divIcon({
            html: `<div style="
              width: ${size}px;
              height: ${size}px;
              border-radius: 50%;
              background: ${backgroundColor};
              border: 3px solid ${borderColor};
              box-shadow: 0 0 20px ${backgroundColor}, 0 4px 6px rgba(0,0,0,0.3);
              display: flex;
              align-items: center;
              justify-content: center;
              color: white;
              font-weight: bold;
              font-size: ${fontSize}px;
              text-shadow: 0 1px 2px rgba(0,0,0,0.5);
              animation: cluster-pulse 2s ease-in-out infinite;
            ">${childCount}</div>`,
            className: `marker-cluster-custom`,
            iconSize: L.point(size, size),
            iconAnchor: L.point(size / 2, size / 2)
          });
        }
      });
      this.map.addLayer(this.markerClusterGroup);

      // Reorder z-index after zoom changes since clusters recalculate
      this.map.on('zoomend', () => {
        setTimeout(() => {
          this.reorderClusterZIndex();
        }, 100);
      });
      
      // Also reorder after marker cluster animation completes
      this.markerClusterGroup.on('animationend', () => {
        this.reorderClusterZIndex();
      });

      // Ensure map is properly displayed after initialization
      const vm = this
      setTimeout(() => {
        vm.map.invalidateSize();
        
        // Always start with Philippines view on initial load
        vm.map.setView(defaultCenter, 4, { animate: false });
        
        // Mark initial load as complete
        vm.initialLoadComplete = true;
      }, 100);
    },
    updateMarkers(merchants) {
      // Clear existing markers
      this.markerClusterGroup.clearLayers();

      // Add new markers for merchants
      merchants.forEach(merchant => {
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

        let merchantLocation = '';
        if (merchant.city) {
          merchantLocation = `${merchant.city}, ${merchant.country}`;
        } else if (merchant.town) {
          merchantLocation = `${merchant.town}, ${merchant.province}, ${merchant.country}`;
        }

        const customIcon = L.icon({
          iconUrl: image,
          iconSize: [35, 48],
          iconAnchor: [17, 48], // Adjusted iconAnchor for proper positioning
        });

        // Fetch latitude and longitude from the related Location object
        const latitude = parseFloat(merchant.latitude);
        const longitude = parseFloat(merchant.longitude);

        // Skip merchants with invalid coordinates
        if (isNaN(latitude) || isNaN(longitude)) {
          return;
        }

        const countryFlag = this.getCountryFlag(merchant.country);

        const marker = L.marker([latitude, longitude], { 
          icon: customIcon,
          zIndexOffset: -1000  // Render behind cluster markers
        })
          .bindPopup(`
          <div class="rounded-lg">
              <div class="flex items-center justify-between">
                  <h3 class="text-lg font-semibold text-gray-900">${merchant.name}</h3>
                  ${merchant.logo ? `<img src="${merchant.logo}" alt="${merchant.name} Logo" class="h-16 w-16 rounded-full">` : ''}
              </div>
              <div class="text-sm md:text-xs">
                  <div class="flex items-center justify-between">
                      <p class="text-gray-600">${merchantLocation}</p>
                      <span class="text-2xl" style="float: right; margin-left: 8px;">${countryFlag}</span>
                  </div>
                  ${merchant.last_transaction_date ? `<p class="text-gray-600">Last transaction: ${timeText}</p>` : ''}
                  <div class="mt-3">
                    <a href="${ this.getGoogleMapLink(merchant) }" target="_blank" class="inline-flex items-center px-3 py-2 text-xs font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200" style="color: white;">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                      </svg>
                      View in Google Map
                    </a>
                  </div>
                  ${merchant.website_url ? `
                    <div class="mt-3">
                      <a href="${merchant.website_url}" target="_blank" class="inline-flex items-center px-3 py-2 text-xs font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200" style="color: white;">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                        </svg>
                        ${merchant.categories?.some(cat => cat.short_name === 'hiverooms') ? 'Book Now' : 'Visit Website'}
                      </a>
                    </div>
                  ` : ''}
              </div>
          </div>
          `);
        this.markerClusterGroup.addLayer(marker);
      });

      // Set z-index on cluster markers after they're created
      this.reorderClusterZIndex();

      // Only auto-fit to markers after initial data load is complete
      if (merchants.length > 0 && !this.isInitialDataLoad && this.initialLoadComplete) {
        this.fitMapToMarkers();
      }
    },
    reorderClusterZIndex() {
      // After clusters are rendered, update z-index so larger clusters appear on top
      const clusterMarkers = document.querySelectorAll('.leaflet-marker-icon');
      clusterMarkers.forEach(marker => {
        // Check if this is a cluster marker
        const clusterDiv = marker.querySelector('.marker-cluster-custom div');
        if (clusterDiv) {
          // Extract the count from the div text
          const count = parseInt(clusterDiv.textContent, 10);
          if (!isNaN(count)) {
            // Set z-index based on cluster size (larger = higher z-index)
            let zIndex = 1000;
            if (count >= 100) {
              zIndex = 4000;
            } else if (count >= 50) {
              zIndex = 3000;
            } else if (count >= 10) {
              zIndex = 2000;
            }
            marker.style.zIndex = zIndex;
          }
        }
      });
    },
    getCountryFlag(country) {
      const countryFlags = {
        'Philippines': '🇵🇭',
        'PH': '🇵🇭',
        'United States': '🇺🇸',
        'USA': '🇺🇸',
        'US': '🇺🇸',
        'Australia': '🇦🇺',
        'AU': '🇦🇺',
        'Canada': '🇨🇦',
        'CA': '🇨🇦',
        'United Kingdom': '🇬🇧',
        'UK': '🇬🇧',
        'GB': '🇬🇧',
        'Singapore': '🇸🇬',
        'SG': '🇸🇬',
        'Japan': '🇯🇵',
        'JP': '🇯🇵',
        'South Korea': '🇰🇷',
        'KR': '🇰🇷',
        'Thailand': '🇹🇭',
        'TH': '🇹🇭',
        'Vietnam': '🇻🇳',
        'VN': '🇻🇳',
        'Malaysia': '🇲🇾',
        'MY': '🇲🇾',
        'Indonesia': '🇮🇩',
        'ID': '🇮🇩',
        'India': '🇮🇳',
        'IN': '🇮🇳',
        'Germany': '🇩🇪',
        'DE': '🇩🇪',
        'France': '🇫🇷',
        'FR': '🇫🇷',
        'Spain': '🇪🇸',
        'ES': '🇪🇸',
        'Italy': '🇮🇹',
        'IT': '🇮🇹',
        'Netherlands': '🇳🇱',
        'NL': '🇳🇱',
        'Switzerland': '🇨🇭',
        'CH': '🇨🇭',
        'Sweden': '🇸🇪',
        'SE': '🇸🇪',
        'Norway': '🇳🇴',
        'NO': '🇳🇴',
        'Denmark': '🇩🇰',
        'DK': '🇩🇰',
        'Finland': '🇫🇮',
        'FI': '🇫🇮',
        'Brazil': '🇧🇷',
        'BR': '🇧🇷',
        'Mexico': '🇲🇽',
        'MX': '🇲🇽',
        'Argentina': '🇦🇷',
        'AR': '🇦🇷',
        'Chile': '🇨🇱',
        'CL': '🇨🇱',
        'Colombia': '🇨🇴',
        'CO': '🇨🇴',
        'South Africa': '🇿🇦',
        'ZA': '🇿🇦',
        'Nigeria': '🇳🇬',
        'NG': '🇳🇬',
        'Kenya': '🇰🇪',
        'KE': '🇰🇪',
        'Ghana': '🇬🇭',
        'GH': '🇬🇭',
        'UAE': '🇦🇪',
        'United Arab Emirates': '🇦🇪',
        'Saudi Arabia': '🇸🇦',
        'SA': '🇸🇦',
        'Turkey': '🇹🇷',
        'TR': '🇹🇷',
        'Israel': '🇮🇱',
        'IL': '🇮🇱',
        'Russia': '🇷🇺',
        'RU': '🇷🇺',
        'China': '🇨🇳',
        'CN': '🇨🇳',
        'Hong Kong': '🇭🇰',
        'HK': '🇭🇰',
        'Taiwan': '🇹🇼',
        'TW': '🇹🇼',
        'New Zealand': '🇳🇿',
        'NZ': '🇳🇿',
        'Portugal': '🇵🇹',
        'PT': '🇵🇹',
        'Belgium': '🇧🇪',
        'BE': '🇧🇪',
        'Austria': '🇦🇹',
        'AT': '🇦🇹',
        'Poland': '🇵🇱',
        'PL': '🇵🇱',
        'Czech Republic': '🇨🇿',
        'CZ': '🇨🇿',
        'Hungary': '🇭🇺',
        'HU': '🇭🇺',
        'Greece': '🇬🇷',
        'GR': '🇬🇷',
        'Ireland': '🇮🇪',
        'IE': '🇮🇪',
        'Ukraine': '🇺🇦',
        'UA': '🇺🇦',
        'Romania': '🇷🇴',
        'RO': '🇷🇴',
        'Bulgaria': '🇧🇬',
        'BG': '🇧🇬',
        'Croatia': '🇭🇷',
        'HR': '🇭🇷',
        'Slovenia': '🇸🇮',
        'SI': '🇸🇮',
        'Slovakia': '🇸🇰',
        'SK': '🇸🇰',
        'Lithuania': '🇱🇹',
        'LT': '🇱🇹',
        'Latvia': '🇱🇻',
        'LV': '🇱🇻',
        'Estonia': '🇪🇪',
        'EE': '🇪🇪',
        'Serbia': '🇷🇸',
        'RS': '🇷🇸',
        'Montenegro': '🇲🇪',
        'ME': '🇲🇪',
        'Bosnia and Herzegovina': '🇧🇦',
        'BA': '🇧🇦',
        'North Macedonia': '🇲🇰',
        'MK': '🇲🇰',
        'Albania': '🇦🇱',
        'AL': '🇦🇱',
        'Kosovo': '🇽🇰',
        'XK': '🇽🇰',
        'Moldova': '🇲🇩',
        'MD': '🇲🇩',
        'Belarus': '🇧🇾',
        'BY': '🇧🇾',
        'Armenia': '🇦🇲',
        'AM': '🇦🇲',
        'Azerbaijan': '🇦🇿',
        'AZ': '🇦🇿',
        'Georgia': '🇬🇪',
        'GE': '🇬🇪',
        'Kazakhstan': '🇰🇿',
        'KZ': '🇰🇿',
        'Uzbekistan': '🇺🇿',
        'UZ': '🇺🇿',
        'Kyrgyzstan': '🇰🇬',
        'KG': '🇰🇬',
        'Tajikistan': '🇹🇯',
        'TJ': '🇹🇯',
        'Turkmenistan': '🇹🇲',
        'TM': '🇹🇲',
        'Mongolia': '🇲🇳',
        'MN': '🇲🇳',
        'Nepal': '🇳🇵',
        'NP': '🇳🇵',
        'Bangladesh': '🇧🇩',
        'BD': '🇧🇩',
        'Sri Lanka': '🇱🇰',
        'LK': '🇱🇰',
        'Pakistan': '🇵🇰',
        'PK': '🇵🇰',
        'Afghanistan': '🇦🇫',
        'AF': '🇦🇫',
        'Iran': '🇮🇷',
        'IR': '🇮🇷',
        'Iraq': '🇮🇶',
        'IQ': '🇮🇶',
        'Syria': '🇸🇾',
        'SY': '🇸🇾',
        'Lebanon': '🇱🇧',
        'LB': '🇱🇧',
        'Jordan': '🇯🇴',
        'JO': '🇯🇴',
        'Kuwait': '🇰🇼',
        'KW': '🇰🇼',
        'Bahrain': '🇧🇭',
        'BH': '🇧🇭',
        'Qatar': '🇶🇦',
        'QA': '🇶🇦',
        'Oman': '🇴🇲',
        'OM': '🇴🇲',
        'Yemen': '🇾🇪',
        'YE': '🇾🇪',
        'Egypt': '🇪🇬',
        'EG': '🇪🇬',
        'Libya': '🇱🇾',
        'LY': '🇱🇾',
        'Tunisia': '🇹🇳',
        'TN': '🇹🇳',
        'Algeria': '🇩🇿',
        'DZ': '🇩🇿',
        'Morocco': '🇲🇦',
        'MA': '🇲🇦',
        'Sudan': '🇸🇩',
        'SD': '🇸🇩',
        'Ethiopia': '🇪🇹',
        'ET': '🇪🇹',
        'Somalia': '🇸🇴',
        'SO': '🇸🇴',
        'Djibouti': '🇩🇯',
        'DJ': '🇩🇯',
        'Eritrea': '🇪🇷',
        'ER': '🇪🇷',
        'Uganda': '🇺🇬',
        'UG': '🇺🇬',
        'Rwanda': '🇷🇼',
        'RW': '🇷🇼',
        'Burundi': '🇧🇮',
        'BI': '🇧🇮',
        'Tanzania': '🇹🇿',
        'TZ': '🇹🇿',
        'Zambia': '🇿🇲',
        'ZM': '🇿🇲',
        'Zimbabwe': '🇿🇼',
        'ZW': '🇿🇼',
        'Malawi': '🇲🇼',
        'MW': '🇲🇼',
        'Mozambique': '🇲🇿',
        'MZ': '🇲🇿',
        'Madagascar': '🇲🇬',
        'MG': '🇲🇬',
        'Mauritius': '🇲🇺',
        'MU': '🇲🇺',
        'Seychelles': '🇸🇨',
        'SC': '🇸🇨',
        'Comoros': '🇰🇲',
        'KM': '🇰🇲',
        'Botswana': '🇧🇼',
        'BW': '🇧🇼',
        'Namibia': '🇳🇦',
        'NA': '🇳🇦',
        'Angola': '🇦🇴',
        'AO': '🇦🇴',
        'Democratic Republic of the Congo': '🇨🇩',
        'DR Congo': '🇨🇩',
        'DRC': '🇨🇩',
        'CD': '🇨🇩',
        'Republic of the Congo': '🇨🇬',
        'Congo': '🇨🇬',
        'CG': '🇨🇬',
        'Gabon': '🇬🇦',
        'GA': '🇬🇦',
        'Equatorial Guinea': '🇬🇶',
        'GQ': '🇬🇶',
        'Cameroon': '🇨🇲',
        'CM': '🇨🇲',
        'Central African Republic': '🇨🇫',
        'CF': '🇨🇫',
        'Chad': '🇹🇩',
        'TD': '🇹🇩',
        'Niger': '🇳🇪',
        'NE': '🇳🇪',
        'Mali': '🇲🇱',
        'ML': '🇲🇱',
        'Burkina Faso': '🇧🇫',
        'BF': '🇧🇫',
        'Senegal': '🇸🇳',
        'SN': '🇸🇳',
        'Gambia': '🇬🇲',
        'GM': '🇬🇲',
        'Guinea-Bissau': '🇬🇼',
        'GW': '🇬🇼',
        'Guinea': '🇬🇳',
        'GN': '🇬🇳',
        'Sierra Leone': '🇸🇱',
        'SL': '🇸🇱',
        'Liberia': '🇱🇷',
        'LR': '🇱🇷',
        'Ivory Coast': '🇨🇮',
        "Côte d'Ivoire": '🇨🇮',
        'CI': '🇨🇮',
        'Togo': '🇹🇬',
        'TG': '🇹🇬',
        'Benin': '🇧🇯',
        'BJ': '🇧🇯',
        'Mauritania': '🇲🇷',
        'MR': '🇲🇷',
        'Cape Verde': '🇨🇻',
        'Cabo Verde': '🇨🇻',
        'CV': '🇨🇻',
        'Sao Tome and Principe': '🇸🇹',
        'ST': '🇸🇹',
        'Lesotho': '🇱🇸',
        'LS': '🇱🇸',
        'Eswatini': '🇸🇿',
        'Swaziland': '🇸🇿',
        'SZ': '🇸🇿',
        'Peru': '🇵🇪',
        'PE': '🇵🇪',
        'Bolivia': '🇧🇴',
        'BO': '🇧🇴',
        'Paraguay': '🇵🇾',
        'PY': '🇵🇾',
        'Uruguay': '🇺🇾',
        'UY': '🇺🇾',
        'Ecuador': '🇪🇨',
        'EC': '🇪🇨',
        'Venezuela': '🇻🇪',
        'VE': '🇻🇪',
        'Guyana': '🇬🇾',
        'GY': '🇬🇾',
        'Suriname': '🇸🇷',
        'SR': '🇸🇷',
        'French Guiana': '🇬🇫',
        'GF': '🇬🇫',
        'Belize': '🇧🇿',
        'BZ': '🇧🇿',
        'Guatemala': '🇬🇹',
        'GT': '🇬🇹',
        'Honduras': '🇭🇳',
        'HN': '🇭🇳',
        'El Salvador': '🇸🇻',
        'SV': '🇸🇻',
        'Nicaragua': '🇳🇮',
        'NI': '🇳🇮',
        'Costa Rica': '🇨🇷',
        'CR': '🇨🇷',
        'Panama': '🇵🇦',
        'PA': '🇵🇦',
        'Cuba': '🇨🇺',
        'CU': '🇨🇺',
        'Jamaica': '🇯🇲',
        'JM': '🇯🇲',
        'Haiti': '🇭🇹',
        'HT': '🇭🇹',
        'Dominican Republic': '🇩🇴',
        'DO': '🇩🇴',
        'Puerto Rico': '🇵🇷',
        'PR': '🇵🇷',
        'Trinidad and Tobago': '🇹🇹',
        'TT': '🇹🇹',
        'Barbados': '🇧🇧',
        'BB': '🇧🇧',
        'Saint Lucia': '🇱🇨',
        'LC': '🇱🇨',
        'Grenada': '🇬🇩',
        'GD': '🇬🇩',
        'Saint Vincent and the Grenadines': '🇻🇨',
        'VC': '🇻🇨',
        'Antigua and Barbuda': '🇦🇬',
        'AG': '🇦🇬',
        'Dominica': '🇩🇲',
        'DM': '🇩🇲',
        'Saint Kitts and Nevis': '🇰🇳',
        'KN': '🇰🇳',
        'Bahamas': '🇧🇸',
        'BS': '🇧🇸',
        'Cayman Islands': '🇰🇾',
        'KY': '🇰🇾',
        'Bermuda': '🇧🇲',
        'BM': '🇧🇲',
        'Aruba': '🇦🇼',
        'AW': '🇦🇼',
        'Curacao': '🇨🇼',
        'CW': '🇨🇼',
        'Sint Maarten': '🇸🇽',
        'SX': '🇸🇽',
        'US Virgin Islands': '🇻🇮',
        'VI': '🇻🇮',
        'British Virgin Islands': '🇻🇬',
        'VG': '🇻🇬',
        'Anguilla': '🇦🇮',
        'AI': '🇦🇮',
        'Montserrat': '🇲🇸',
        'MS': '🇲🇸',
        'Guadeloupe': '🇬🇵',
        'GP': '🇬🇵',
        'Martinique': '🇲🇶',
        'MQ': '🇲🇶',
        'Saint Barthelemy': '🇧🇱',
        'BL': '🇧🇱',
        'Saint Martin': '🇲🇫',
        'MF': '🇲🇫',
        'Sint Eustatius': '🇧🇶',
        'BQ': '🇧🇶',
        'Saba': '🇧🇶',
        'Saint Pierre and Miquelon': '🇵🇲',
        'PM': '🇵🇲',
        'Greenland': '🇬🇱',
        'GL': '🇬🇱',
        'Falkland Islands': '🇫🇰',
        'FK': '🇫🇰',
        'South Georgia and the South Sandwich Islands': '🇬🇸',
        'GS': '🇬🇸',
        'Antarctica': '🇦🇶',
        'AQ': '🇦🇶'
      };
      return countryFlags[country] || '🏳️';
    },
    getGoogleMapLink(merchant) {
      if (merchant.gmap_business_link) {
        return merchant.gmap_business_link
      } else {
        return `https://www.google.com/maps?q=${merchant.latitude},${merchant.longitude}`
      }
    },
    centerOnTarget(coordinates, zoomLevel, onComplete) {
      if (coordinates.length == 0) {
        coordinates = defaultCenter;
      }
      // Invalidate size first to ensure proper rendering after container becomes visible
      this.map.invalidateSize();
      // Use flyTo for smoother transition
      this.map.flyTo(coordinates, zoomLevel, { animate: true, duration: 1.2 });
      
      // If a callback is provided, listen for the moveend event (fires when animation completes)
      if (onComplete && typeof onComplete === 'function') {
        const handleMoveEnd = () => {
          onComplete();
          this.map.off('moveend', handleMoveEnd);
        };
        this.map.once('moveend', handleMoveEnd);
      }
    },
    openPopup(latitude, longitude, content) {
      const popup = L.popup()
        .setLatLng([latitude, longitude])
        .setContent(content);
      popup.openOn(this.map);
    },
    fitMapToViewport() {
      // Get the map container dimensions
      const container = this.$refs.map;
      const containerHeight = container.clientHeight;
      
      // Use a more direct approach to fill the viewport
      // Start with a reasonable zoom level and adjust based on container size
      let zoomLevel = 4; // Start with zoom level 4
      
      // If container is tall, increase zoom to fill vertical space
      if (containerHeight > 600) {
        zoomLevel = 5;
      }
      if (containerHeight > 800) {
        zoomLevel = 6;
      }
      if (containerHeight > 1000) {
        zoomLevel = 7;
      }
      
      // Center the map and set the calculated zoom
      this.map.setView(defaultCenter, zoomLevel, { animate: false });
    },
    
    // Public method to fit viewport when map becomes visible (e.g., on mobile)
    fitViewportWhenVisible() {
      // Wait for the map container to be fully visible in the DOM
      setTimeout(() => {
        // Invalidate size first - this is critical for Leaflet to recalculate
        // tiles when the container was previously hidden (display: none)
        this.map.invalidateSize();
        
        // Then fit to markers after size is recalculated
        if (this.merchants && this.merchants.length > 0) {
          this.fitMapToMarkers();
        } else {
          this.map.setView(defaultCenter, 4, { animate: false });
        }
      }, 100);
    },
    fitMapToMarkers() {
      // Get all markers from the cluster group
      const markers = this.markerClusterGroup.getLayers();
      
      if (markers.length > 0) {
        // Create a group of all markers to calculate bounds
        const group = L.featureGroup(markers);
        
        // Fit the map to show all markers with some padding
        this.map.fitBounds(group.getBounds(), {
          padding: [20, 20], // Add 20px padding around the bounds
          maxZoom: 12, // Limit maximum zoom to prevent over-zooming
          animate: true,
          duration: 1.5
        });
      }
    },
  },
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
  min-height: 100vh;
}

.map-container .leaflet-container {
  height: 100% !important;
  width: 100% !important;
}
</style>

<style>
/* Cluster pulse animation */
@keyframes cluster-pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

/* Custom cluster marker styling */
.marker-cluster-custom {
  background: transparent !important;
}

.marker-cluster-custom div {
  transition: all 0.3s ease;
}

.marker-cluster-custom:hover div {
  transform: scale(1.1) !important;
  filter: brightness(1.1);
}

/* Make individual pins more visible when clustered */
.leaflet-marker-icon {
  transition: transform 0.3s ease;
}

/* Spiderfy effect - when clicking on cluster */
.leaflet-cluster-spider-leg {
  stroke: #22c55e;
  stroke-width: 2;
  stroke-opacity: 0.6;
}

/* Popup ease-in animation from below */
.leaflet-popup {
  animation: popup-ease-up 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  transform-origin: bottom center;
}

@keyframes popup-ease-up {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Popup content wrapper animation */
.leaflet-popup-content-wrapper {
  animation: popup-content-fade 0.3s ease-out 0.1s both;
}

@keyframes popup-content-fade {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

</style>
