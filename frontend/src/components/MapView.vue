<template>
  <div class="map-container w-full h-full">
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


// Default map center is Tacloban City
const defaultCenter = [11.2441900, 124.9987370];

export default {
  name: 'MapView',
  props: {
    merchants: {
      type: Array,
      default: () => [],
    },
  },
  mounted() {
    this.loadMap();
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
      this.map = L.map(this.$refs.map).setView(defaultCenter, 8);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);

      // Initialize marker cluster group
      this.markerClusterGroup = L.markerClusterGroup();
      this.map.addLayer(this.markerClusterGroup);
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

        const marker = L.marker([latitude, longitude], { icon: customIcon })
          .bindPopup(`
          <div class="sm:w-full rounded-lg">
              <div class="flex items-center justify-between">
                  <h3 class="font-semibold">${merchant.name}</h3>
                  <img src="${merchant.logo}" alt="${merchant.name} Logo" class="h-16 w-16 rounded-full">
              </div>
              <p>${merchantLocation}</p>
              <p>Last transaction: ${timeText}</p>
              <a href="${ this.getGoogleMapLink(merchant) }" target="_blank" class="text-blue-500 hover:underline">View in Google Map</a>
          </div>
          `);
        this.markerClusterGroup.addLayer(marker);
      });
    },
    getGoogleMapLink(merchant) {
      if (merchant.gmap_business_link) {
        return merchant.gmap_business_link
      } else {
        return `https://www.google.com/maps?q=${merchant.latitude},${merchant.longitude}`
      }
    },
    centerOnTarget(coordinates, zoomLevel) {
      if (coordinates.length == 0) {
        coordinates = defaultCenter;
      } 
      this.map.setView(coordinates, zoomLevel, { animate: true, duration: 1.5 }); 
    },
    openPopup(latitude, longitude, content) {
      const popup = L.popup()
        .setLatLng([latitude, longitude])
        .setContent(content);
      popup.openOn(this.map);
    },
  },
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
}
</style>
