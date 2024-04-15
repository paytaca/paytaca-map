<template>
  <div class="map-container w-full h-full">
    <div id="map" class="w-full h-full"></div>
  </div>
</template>

<script>
/* eslint-disable */
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

export default {
  name: 'MapView',
  mounted() {
    this.loadMap();
    this.fetchMarkers();
  },
  methods: {
    loadMap() {
      this.map = L.map('map').setView([11.2441900, 124.9987370], 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
    },
    fetchMarkers() {
      axios.get('http://localhost:8000/locations/') // Change URL as per your Django server address
        .then(response => {
          const locations = response.data; // Response data directly contains locations
          locations.forEach(location => {
            const transactionDate = new Date(location.last_transaction_date);
            const currentDate = new Date();
            const weeksAgo = Math.round((currentDate - transactionDate) / (1000 * 60 * 60 * 24 * 7)); // Calculate weeks difference
            const lastTransactionText = weeksAgo === 1 ? '1 week ago' : `${weeksAgo} weeks ago`;

            const customIcon = L.icon({
              iconUrl: require('@/assets/marker_pin.png'), // Path to your custom marker icon
              iconSize: [38, 38], // Adjust the size if needed
              iconAnchor: [19, 38], // Adjust the anchor if needed
            });

            const popupContent = `
              <div>
                <h3>${location.name}</h3>
                <p>Last transaction: ${lastTransactionText}</p>
                <a href="${location.gmap_business_link}" target="_blank">View in Google Map</a>
              </div>
            `;
            L.marker([location.latitude, location.longitude], { icon: customIcon })
              .bindPopup(popupContent)
              .addTo(this.map);
          });
        })
        .catch(error => {
          console.error('Error fetching locations:', error);
        });
    }
  }
};
</script>

<style scoped>
.map-container {
  width: 100vw; /* Change width to full viewport width */
  height: 100vh; /* Change height to full viewport height */
}

#map {
  width: 100%;
  height: 100%;
}
</style>
