<template>
  <div class="map-container w-full h-full">
    <div id="map" class="w-full h-full"></div>
  </div>
</template>

<script>
/* eslint-disable */
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet.markercluster/dist/leaflet.markercluster';
import image from "../assets/marker_pin.png"
import axios from 'axios';

export default {
  name: 'MapView',
  mounted() {
    this.loadMap();
    this.fetchMarkers();
  },
  methods: {
    loadMap() {
      this.map = L.map('map').setView([11.2441900, 124.9987370], 10);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
    },
    fetchMarkers() {
      axios.get('http://localhost:8000/locations/')
        .then(response => {
          const locations = response.data;
          const markers = L.markerClusterGroup({
            maxClusterRadius: 50,
            disableClusteringAtZoom: 13,
          });
          locations.forEach(location => {
            const transactionDate = new Date(location.last_transaction_date);
            const currentDate = new Date();
            const weeksAgo = Math.round((currentDate - transactionDate) / (1000 * 60 * 60 * 24 * 7));
            const lastTransactionText = weeksAgo === 1 ? '1 week ago' : `${weeksAgo} weeks ago`;

            const customIcon = L.icon({
              iconUrl: image,
              iconSize: [35, 48],
              iconAnchor: [24, 48],
            });

            const popupContent = `
              <div>
                <h3>${location.name}</h3>
                <p>Last transaction: ${lastTransactionText}</p>
                <a href="${location.gmap_business_link}" target="_blank">View in Google Map</a>
              </div>
            `;
            const marker = L.marker([location.latitude, location.longitude], { icon: customIcon })
              .bindPopup(popupContent);
            markers.addLayer(marker);
          });
          this.map.addLayer(markers);
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
  width: 100%;
  height: 100%;
}
</style>
