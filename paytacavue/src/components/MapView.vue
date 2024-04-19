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
import image from "../assets/marker_pin.png"

export default {
  name: 'MapView',
  props: {
    locations: {
      type: Array,
      default: () => [],
    },
  },
  mounted() {
    this.loadMap();
  },
  watch: {
    locations: {
      handler(newLocations) {
        this.updateMarkers(newLocations);
      },
      deep: true,
    },
  },
  methods: {
    loadMap() {
      this.map = L.map(this.$refs.map).setView([11.2441900, 124.9987370], 10);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);

      // Initialize marker cluster group
      this.markerClusterGroup = L.markerClusterGroup();
      this.map.addLayer(this.markerClusterGroup);
    },
    updateMarkers(locations) {
      // Clear existing markers
      this.markerClusterGroup.clearLayers();

      // Add new markers for locations
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

        const marker = L.marker([location.latitude, location.longitude], { icon: customIcon })
          .bindPopup(`
            <div>
              <h3>${location.name}</h3>
              <p>${location.location}, ${location.city}, ${location.country}</p>
              <p>Last transaction: ${lastTransactionText}</p>
              <a href="${location.gmap_business_link}" target="_blank">View in Google Map</a>
            </div>
          `);
        this.markerClusterGroup.addLayer(marker);
      });
    },
    setCenter(latitude, longitude) {
      this.map.setView([latitude, longitude], 30); // Adjust the zoom level as needed
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
