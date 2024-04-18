<template>
  <div class="map-container w-full h-full">
    <div id="map" class="w-full h-full"></div>
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
      this.map = L.map('map').setView([11.2441900, 124.9987370], 10);
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
        const customIcon = L.icon({
          iconUrl: image,
          iconSize: [35, 48],
          iconAnchor: [24, 48],
        });

        const popupContent = `
          <div>
            <h3>${location.name}</h3>
            <p>${location.location}, ${location.city}, ${location.country}</p>
          </div>
        `;
        const marker = L.marker([location.latitude, location.longitude], { icon: customIcon })
          .bindPopup(popupContent);
        this.markerClusterGroup.addLayer(marker);
      });
    },
    setCenter(latitude, longitude) {
      this.map.setView([latitude, longitude], 15); // Adjust the zoom level as needed
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
