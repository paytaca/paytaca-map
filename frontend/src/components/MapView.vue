<template>
  <div class="map-container w-full h-full relative">
    <div ref="map" class="w-full h-full"></div>

    <div v-if="mapError" class="map-error" role="alert">
      <p class="map-error__title">Map unavailable</p>
      <p class="map-error__text">{{ mapError }}</p>
    </div>

    <button
      v-if="showGlobeButton"
      type="button"
      class="globe-home-btn"
      title="Back to globe view"
      aria-label="Back to globe view"
      @click="returnToGlobeFit"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18" />
        <path d="M12 3c2.6 2.4 4 5.6 4 9s-1.4 6.6-4 9c-2.6-2.4-4-5.6-4-9s1.4-6.6 4-9Z" />
      </svg>
    </button>
  </div>
</template>

<script>
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import image from "../assets/marker_pin.png";

// Default map center - Philippines ([lng, lat] for MapLibre)
const defaultCenter = [121.7740, 12.8797];
// const defaultCenter = [124.9987370, 11.2441900]; // Tacloban City
// const defaultCenter = [129.97266776311113, -2.745453205711577]; // Custom

const GLYPHS_URL = 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf';

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
      mapError: null,
      popup: null,
      featureHtmlById: {},
      clusterMinPointsZoomedOut: 1,
      clusterMinPointsCloseup: 20,
      clusterCloseupZoomThreshold: 10,
      appliedClusterMinPoints: null,
      currentFeatureCollection: { type: 'FeatureCollection', features: [] },
      clusterPulseFrame: null,
      globeResizeObserver: null,
      initResizeObserver: null,
      globeFitZoom: null,
      spinFrame: null,
      spinLastTime: 0,
      spinDegreesPerSecond: 2.5,
      spinUserPaused: false,
      spinResumeTimeout: null,
      spinInternalMove: false,
      isSpinning: false,
      travelPauseMs: 700,
      travelPauseTimeout: null,
      travelMoveHandler: null,
      mapZoom: null,
    };
  },
  mounted() {
    this.loadMap();
    window.addEventListener('themechange', this.onThemeChange);
    // After 3 seconds, consider initial data load complete
    setTimeout(() => {
      this.isInitialDataLoad = false;
    }, 3000);
  },
  beforeUnmount() {
    window.removeEventListener('themechange', this.onThemeChange);
    this.stopClusterPulse();
    this.stopGlobeSpin();
    if (this.spinResumeTimeout) {
      clearTimeout(this.spinResumeTimeout);
      this.spinResumeTimeout = null;
    }
    if (this.travelPauseTimeout) {
      clearTimeout(this.travelPauseTimeout);
      this.travelPauseTimeout = null;
    }
    if (this.travelMoveHandler && this.map) {
      this.map.off('moveend', this.travelMoveHandler);
      this.travelMoveHandler = null;
    }
    if (this.globeResizeObserver) {
      this.globeResizeObserver.disconnect();
      this.globeResizeObserver = null;
    }
    if (this.initResizeObserver) {
      this.initResizeObserver.disconnect();
      this.initResizeObserver = null;
    }
    if (this.popup) {
      this.popup.remove();
      this.popup = null;
    }
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  },
  watch: {
    merchants: {
      handler(newMerchants) {
        this.updateMarkers(newMerchants);
      },
      deep: true,
    },
  },
  computed: {
    // Show the globe shortcut whenever the map is zoomed past the globe fit level
    showGlobeButton() {
      return (
        this.globeFitZoom !== null &&
        this.mapZoom !== null &&
        this.mapZoom > this.globeFitZoom + 0.15
      );
    },
  },
  methods: {
    loadMap() {
      const container = this.$refs.map;
      if (!container || this.map) {
        return;
      }

      // On mobile the map panel starts hidden (display: none), so the container
      // has no size yet. Initializing MapLibre into a 0x0 box produces a broken
      // canvas, so wait until the container is actually laid out.
      if ((!container.clientWidth || !container.clientHeight) && typeof ResizeObserver !== 'undefined') {
        if (!this.initResizeObserver) {
          this.initResizeObserver = new ResizeObserver(() => {
            const el = this.$refs.map;
            if (el && el.clientWidth && el.clientHeight) {
              this.initResizeObserver.disconnect();
              this.initResizeObserver = null;
              this.loadMap();
            }
          });
          this.initResizeObserver.observe(container);
        }
        return;
      }

      const fitZoom = this.computeGlobeFitZoom(container.clientWidth, container.clientHeight, defaultCenter[1]);

      // MapLibre GL v5 (globe projection) requires WebGL2. Older iOS/Safari builds
      // only expose WebGL1, which fails silently into a blank canvas.
      if (!this.supportsWebGL2()) {
        this.mapError =
          'This device or browser cannot render the interactive 3D map. Please update to the latest version of iOS or Safari.';
        return;
      }

      this.map = new maplibregl.Map({
        container: this.$refs.map,
        style: {
          version: 8,
          projection: { type: 'globe' },
          glyphs: GLYPHS_URL,
          sources: {
            osm: {
              type: 'raster',
              tiles: [
                'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png',
              ],
              tileSize: 256,
              maxzoom: 19,
              attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            },
          },
          layers: [
            {
              id: 'water',
              type: 'background',
              paint: { 'background-color': '#a5c8e4' },
            },
            {
              id: 'osm',
              type: 'raster',
              source: 'osm',
            },
          ],
        },
        center: defaultCenter,
        zoom: fitZoom ?? 4,
        maxZoom: 19,
        attributionControl: { compact: true },
      });

      // Globe opens fully visible and cannot be zoomed out past that fit level
      if (fitZoom !== null) {
        this.map.setMinZoom(fitZoom);
      }
      this.globeFitZoom = fitZoom;
      this.mapZoom = this.map.getZoom();

      // Re-cluster with a different minimum size depending on zoom level
      this.map.on('zoomend', () => {
        this.mapZoom = this.map.getZoom();
        this.syncClusterMinPoints();
        this.scheduleGlobeSpinResume();
      });

      // Keep the zoom-out limit in sync with the globe's rendered size, and
      // resume auto-rotation once the viewer settles back at the fit level
      this.map.on('moveend', () => {
        if (this.spinInternalMove) {
          return;
        }
        this.updateGlobeMinZoom();
        this.scheduleGlobeSpinResume();
      });

      // Pause auto-rotation as soon as the user interacts with the globe
      ['movestart', 'zoomstart', 'rotatestart', 'pitchstart'].forEach((event) => {
        this.map.on(event, () => {
          if (!this.spinInternalMove) {
            this.pauseGlobeSpin();
          }
        });
      });

      this.map.on('load', () => {
        this.map
          .loadImage(image)
          .then((response) => {
            if (!this.map.hasImage('merchant-pin')) {
              this.map.addImage('merchant-pin', response.data);
            }
          })
          .catch(() => {})
          .finally(() => {
            this.setupMerchantLayers();
            this.updateMarkers(this.merchants);
          });

        // Mark initial load as complete
        setTimeout(() => {
          this.initialLoadComplete = true;
        }, 100);

        // Limit zoom-out so the globe always fits the container
        this.updateGlobeMinZoom();
        this.setupGlobeResizeObserver();

        // Match the basemap to the active color scheme
        this.applyMapTheme(this.isDarkTheme());

        // Start the slow Earth-like rotation at the fit zoom level
        this.evaluateGlobeSpin();
      });
    },
    isDarkTheme() {
      return document.documentElement.classList.contains('dark');
    },
    supportsWebGL2() {
      try {
        const canvas = document.createElement('canvas');
        return !!canvas.getContext('webgl2');
      } catch (e) {
        void e;
        return false;
      }
    },
    applyMapTheme(dark) {
      if (!this.map) {
        return;
      }
      if (this.map.getLayer('water')) {
        this.map.setPaintProperty('water', 'background-color', dark ? '#12233d' : '#a5c8e4');
      }
      if (this.map.getLayer('osm')) {
        if (dark) {
          this.map.setPaintProperty('osm', 'raster-brightness-max', 0.62);
          this.map.setPaintProperty('osm', 'raster-saturation', -0.28);
          this.map.setPaintProperty('osm', 'raster-contrast', 0.12);
        } else {
          this.map.setPaintProperty('osm', 'raster-brightness-max', 1);
          this.map.setPaintProperty('osm', 'raster-saturation', 0);
          this.map.setPaintProperty('osm', 'raster-contrast', 0);
        }
      }
    },
    onThemeChange(event) {
      const dark = event && event.detail ? event.detail.dark : this.isDarkTheme();
      this.applyMapTheme(dark);
    },
    computeGlobeFitZoom(width, height, lat) {
      if (!width || !height) {
        return null;
      }
      // MapLibre renders the globe as a sphere of radius (px):
      //   worldSize / (2 * PI) / cos(centerLat),  where worldSize = 512 * 2^zoom
      // Solve for the zoom where the diameter matches the shorter container edge.
      const latFactor = Math.cos((lat * Math.PI) / 180);
      const targetRadius = Math.min(width, height) / 2;
      const zoom = Math.log2((targetRadius * 2 * Math.PI * latFactor) / 512);
      return isFinite(zoom) ? Math.max(zoom, 0) : null;
    },
    updateGlobeMinZoom() {
      if (!this.map || this.isSpinning) {
        return;
      }
      const container = this.map.getContainer();
      const clamped = this.computeGlobeFitZoom(
        container.clientWidth,
        container.clientHeight,
        this.map.getCenter().lat,
      );
      if (clamped === null) {
        return;
      }
      this.globeFitZoom = clamped;
      this.map.setMinZoom(clamped);
      if (this.map.getZoom() < clamped - 0.01) {
        this.map.setZoom(clamped);
      }
    },
    setupGlobeResizeObserver() {
      if (this.globeResizeObserver || typeof ResizeObserver === 'undefined') {
        return;
      }
      this.globeResizeObserver = new ResizeObserver(() => {
        if (this.map) {
          this.map.resize();
        }
        this.updateGlobeMinZoom();
      });
      this.globeResizeObserver.observe(this.$refs.map);
    },
    isAtGlobeFitZoom() {
      if (!this.map || this.globeFitZoom === null) {
        return false;
      }
      return this.map.getZoom() <= this.globeFitZoom + 0.05;
    },
    startGlobeSpin() {
      if (!this.map || this.isSpinning || this.spinUserPaused) {
        return;
      }
      this.isSpinning = true;
      this.spinLastTime = 0;
      this.spinFrame = requestAnimationFrame(this.spinStep);
    },
    stopGlobeSpin() {
      this.isSpinning = false;
      if (this.spinFrame !== null) {
        cancelAnimationFrame(this.spinFrame);
        this.spinFrame = null;
      }
      this.spinLastTime = 0;
    },
    spinStep(now) {
      if (!this.map || !this.isSpinning) {
        return;
      }
      if (!this.spinLastTime) {
        this.spinLastTime = now;
      }
      const deltaSeconds = (now - this.spinLastTime) / 1000;
      this.spinLastTime = now;

      const center = this.map.getCenter();
      // Earth rotates west -> east, so surface features drift east (right) while
      // the point under the camera keeps moving west: decrease the center longitude.
      let longitude = center.lng - this.spinDegreesPerSecond * deltaSeconds;
      if (longitude < -180) {
        longitude += 360;
      }

      this.spinInternalMove = true;
      this.map.setCenter([longitude, center.lat]);
      this.spinInternalMove = false;

      this.spinFrame = requestAnimationFrame(this.spinStep);
    },
    pauseGlobeSpin() {
      this.spinUserPaused = true;
      this.stopGlobeSpin();
      this.scheduleGlobeSpinResume();
    },
    scheduleGlobeSpinResume() {
      if (this.spinResumeTimeout) {
        clearTimeout(this.spinResumeTimeout);
      }
      this.spinResumeTimeout = setTimeout(() => {
        this.spinResumeTimeout = null;
        this.spinUserPaused = false;
        this.evaluateGlobeSpin();
      }, 3000);
    },
    evaluateGlobeSpin() {
      if (this.isAtGlobeFitZoom()) {
        this.startGlobeSpin();
      } else {
        this.stopGlobeSpin();
      }
    },
    getClusterMinPointsForZoom(zoom) {
      return zoom >= this.clusterCloseupZoomThreshold
        ? this.clusterMinPointsCloseup
        : this.clusterMinPointsZoomedOut;
    },
    syncClusterMinPoints() {
      if (!this.map || !this.map.getSource('merchants')) {
        return;
      }
      const desired = this.getClusterMinPointsForZoom(this.map.getZoom());
      if (desired === this.appliedClusterMinPoints) {
        return;
      }
      // Cluster options are fixed at source-creation time in MapLibre, so rebuild the source
      ['unclustered-count', 'unclustered-circle', 'unclustered-halo', 'cluster-count', 'unclustered', 'clusters', 'cluster-halo'].forEach((id) => {
        if (this.map.getLayer(id)) {
          this.map.removeLayer(id);
        }
      });
      if (this.map.getSource('merchants')) {
        this.map.removeSource('merchants');
      }
      this.setupMerchantLayers(desired);
    },
    setupMerchantLayers(minPoints = this.getClusterMinPointsForZoom(this.map.getZoom())) {
      this.appliedClusterMinPoints = minPoints;
      this.map.addSource('merchants', {
        type: 'geojson',
        data: this.currentFeatureCollection,
        cluster: true,
        clusterMaxZoom: 14,
        clusterRadius: 50,
        clusterMinPoints: minPoints,
      });

      this.map.addLayer({
        id: 'clusters',
        type: 'circle',
        source: 'merchants',
        filter: ['has', 'point_count'],
        paint: {
          'circle-color': 'rgba(34, 197, 94, 0.7)',
          'circle-radius': ['step', ['get', 'point_count'], 18, 10, 23, 50, 28, 100, 33],
          'circle-stroke-width': 3,
          'circle-stroke-color': '#16a34a',
        },
      });

      this.map.addLayer({
        id: 'cluster-count',
        type: 'symbol',
        source: 'merchants',
        filter: ['has', 'point_count'],
        layout: {
          'text-field': '{point_count_abbreviated}',
          'text-font': ['Open Sans Bold'],
          'text-size': 14,
          'text-allow-overlap': true,
        },
        paint: { 'text-color': '#ffffff' },
      });

      this.map.addLayer({
        id: 'unclustered',
        type: 'symbol',
        source: 'merchants',
        minzoom: this.clusterCloseupZoomThreshold,
        filter: ['!', ['has', 'point_count']],
        layout: {
          'icon-image': 'merchant-pin',
          'icon-size': [
            'interpolate', ['linear'], ['zoom'],
            3, 0.2,
            6, 0.35,
            10, 0.6,
            14, 0.9,
            18, 1,
          ],
          'icon-anchor': 'bottom',
          'icon-allow-overlap': true,
          'icon-ignore-placement': true,
        },
      });

      // Lone merchants are not clustered by supercluster, so at zoomed-out levels we
      // render them as a cluster-style circle labeled "1" for a uniform expectation.
      this.map.addLayer({
        id: 'unclustered-circle',
        type: 'circle',
        source: 'merchants',
        maxzoom: this.clusterCloseupZoomThreshold,
        filter: ['!', ['has', 'point_count']],
        paint: {
          'circle-color': 'rgba(34, 197, 94, 0.7)',
          'circle-radius': 18,
          'circle-stroke-width': 3,
          'circle-stroke-color': '#16a34a',
        },
      });

      this.map.addLayer({
        id: 'unclustered-count',
        type: 'symbol',
        source: 'merchants',
        maxzoom: this.clusterCloseupZoomThreshold,
        filter: ['!', ['has', 'point_count']],
        layout: {
          'text-field': '1',
          'text-font': ['Open Sans Bold'],
          'text-size': 14,
          'text-allow-overlap': true,
        },
        paint: { 'text-color': '#ffffff' },
      });

      // Pulsing halos behind clusters (and lone-merchant circles) for a throbbing/shining effect.
      // Their radius/opacity are animated by startClusterPulse().
      this.map.addLayer({
        id: 'cluster-halo',
        type: 'circle',
        source: 'merchants',
        filter: ['has', 'point_count'],
        paint: {
          'circle-color': '#22c55e',
          'circle-radius': ['step', ['get', 'point_count'], 18, 10, 23, 50, 28, 100, 33],
          'circle-opacity': 0.4,
          'circle-radius-transition': { duration: 0, delay: 0 },
          'circle-opacity-transition': { duration: 0, delay: 0 },
        },
      }, 'clusters');

      this.map.addLayer({
        id: 'unclustered-halo',
        type: 'circle',
        source: 'merchants',
        maxzoom: this.clusterCloseupZoomThreshold,
        filter: ['!', ['has', 'point_count']],
        paint: {
          'circle-color': '#22c55e',
          'circle-radius': 18,
          'circle-opacity': 0.4,
          'circle-radius-transition': { duration: 0, delay: 0 },
          'circle-opacity-transition': { duration: 0, delay: 0 },
        },
      }, 'unclustered-circle');

      this.startClusterPulse();

      // Clicking a cluster zooms in to expand it
      this.map.on('click', 'clusters', (e) => {
        const features = this.map.queryRenderedFeatures(e.point, { layers: ['clusters'] });
        if (!features.length) {
          return;
        }
        const clusterId = features[0].properties.cluster_id;
        this.map.getSource('merchants').getClusterExpansionZoom(clusterId).then((zoom) => {
          this.map.easeTo({ center: features[0].geometry.coordinates, zoom });
        }).catch(() => {});
      });

      // Clicking a pin opens its popup
      const openMerchantPopup = (e) => {
        const feature = e.features[0];
        const html = this.featureHtmlById[feature.properties.id];
        if (!html) {
          return;
        }
        if (this.popup) {
          this.popup.remove();
        }
        this.popup = new maplibregl.Popup({ offset: [0, -48], maxWidth: '360px' })
          .setLngLat(feature.geometry.coordinates)
          .setHTML(html)
          .addTo(this.map);
      };
      this.map.on('click', 'unclustered', openMerchantPopup);

      // Clicking a lone merchant (shown as a "cluster of 1") zooms in like a cluster,
      // where it will then appear as a normal pin.
      this.map.on('click', 'unclustered-circle', (e) => {
        this.map.easeTo({
          center: e.features[0].geometry.coordinates,
          zoom: this.clusterCloseupZoomThreshold,
        });
      });

      ['clusters', 'unclustered', 'unclustered-circle'].forEach((layer) => {
        this.map.on('mouseenter', layer, () => {
          this.map.getCanvas().style.cursor = 'pointer';
        });
        this.map.on('mouseleave', layer, () => {
          this.map.getCanvas().style.cursor = '';
        });
      });
    },
    startClusterPulse() {
      if (this.clusterPulseFrame) {
        return;
      }
      const baseRadius = ['step', ['get', 'point_count'], 18, 10, 23, 50, 28, 100, 33];
      const period = 1600;
      const tick = (time) => {
        if (!this.map) {
          return;
        }
        const phase = 0.5 - 0.5 * Math.cos((time / period) * Math.PI * 2); // 0 -> 1 -> 0
        const extra = 2 + 12 * phase;
        const opacity = 0.05 + 0.4 * (1 - phase);

        if (this.map.getLayer('cluster-halo')) {
          this.map.setPaintProperty('cluster-halo', 'circle-radius', ['+', baseRadius, extra]);
          this.map.setPaintProperty('cluster-halo', 'circle-opacity', opacity);
        }
        if (this.map.getLayer('unclustered-halo')) {
          this.map.setPaintProperty('unclustered-halo', 'circle-radius', 18 + extra);
          this.map.setPaintProperty('unclustered-halo', 'circle-opacity', opacity);
        }
        this.clusterPulseFrame = requestAnimationFrame(tick);
      };
      this.clusterPulseFrame = requestAnimationFrame(tick);
    },
    stopClusterPulse() {
      if (this.clusterPulseFrame) {
        cancelAnimationFrame(this.clusterPulseFrame);
        this.clusterPulseFrame = null;
      }
    },
    updateMarkers(merchants) {
      const features = [];
      this.featureHtmlById = {};

      (merchants || []).forEach((merchant) => {
        const latitude = parseFloat(merchant.latitude);
        const longitude = parseFloat(merchant.longitude);

        // Skip merchants with invalid coordinates
        if (isNaN(latitude) || isNaN(longitude)) {
          return;
        }

        this.featureHtmlById[merchant.id] = this.buildMerchantPopupHtml(merchant);
        features.push({
          type: 'Feature',
          geometry: { type: 'Point', coordinates: [longitude, latitude] },
          properties: {
            id: merchant.id,
            verified: !!merchant.verified,
          },
        });
      });

      const source = this.map && this.map.getSource('merchants');
      this.currentFeatureCollection = { type: 'FeatureCollection', features };
      if (source) {
        source.setData(this.currentFeatureCollection);
      }

      // Only auto-fit to markers after initial data load is complete
      if (features.length > 0 && !this.isInitialDataLoad && this.initialLoadComplete) {
        this.fitMapToMarkers();
      }
    },
    buildMerchantPopupHtml(merchant) {
      const transactionDate = new Date(merchant.last_transaction_date);
      const currentDate = new Date();
      const timeDifference = currentDate - transactionDate;
      let timeText = '';

      const years = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365));
      const months = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 30));
      const weeks = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 7));
      const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
      const hours = Math.floor(timeDifference / (1000 * 60 * 60));
      const minutes = Math.floor(timeDifference / (1000 * 60));

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

      const countryFlag = this.getCountryFlag(merchant.country);
      const locationText = merchantLocation || merchant.country || '';

      return `
          <div class="min-w-[260px] max-w-[320px]">
              <div class="flex items-start gap-3">
                  <div class="min-w-0 flex-1">
                      <h3 class="truncate text-base font-semibold text-ink">${merchant.name}</h3>
                      ${locationText ? `<p class="mt-1 flex items-start gap-1.5 text-sm text-ink-muted">
                          <span class="w-5 shrink-0 text-center leading-5">${countryFlag}</span>
                          <span class="truncate">${locationText}</span>
                      </p>` : ''}
                      ${merchant.last_transaction_date ? `<p class="mt-0.5 text-sm text-ink-faint">Last transaction: ${timeText}</p>` : ''}
                  </div>
                  ${merchant.logo ? `<img src="${merchant.logo}" alt="${merchant.name} Logo" class="h-14 w-14 shrink-0 rounded-full object-cover ring-1 ring-brand-100">` : ''}
              </div>
              <div class="mt-4 flex flex-wrap gap-2 border-t border-soft pt-3">
                  <a href="${this.getGoogleMapLink(merchant)}" target="_blank" class="inline-flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-medium text-white transition-colors duration-200 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                      </svg>
                      View in Google Map
                  </a>
                  ${merchant.website_url ? `
                      <a href="${merchant.website_url}" target="_blank" class="inline-flex items-center gap-1.5 rounded-lg bg-sky-600 px-3 py-1.5 text-xs font-medium text-white transition-colors duration-200 hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                        </svg>
                        ${merchant.categories?.some(cat => cat.short_name === 'hiverooms') ? 'Book Now' : 'Visit Website'}
                      </a>
                  ` : ''}
              </div>
          </div>
          `;
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
      if (!this.map) {
        return;
      }

      // Coordinates arrive as [lat, lng]; MapLibre expects [lng, lat]
      let lat = coordinates && coordinates.length ? parseFloat(coordinates[0]) : NaN;
      let lng = coordinates && coordinates.length ? parseFloat(coordinates[1]) : NaN;
      if (isNaN(lat) || isNaN(lng)) {
        lng = defaultCenter[0];
        lat = defaultCenter[1];
      }

      // Ensure proper rendering after container becomes visible
      this.map.resize();
      const targetZoom = zoomLevel || 4;
      this.map.flyTo({
        center: [lng, lat],
        zoom: targetZoom,
        duration: this.computeFlightDuration(lat, lng, targetZoom),
      });

      // If a callback is provided, fire it once the movement finishes
      if (onComplete && typeof onComplete === 'function') {
        this.map.once('moveend', onComplete);
      }
    },
    // Scale flight time with distance and zoom change so long ocean-crossing
    // flights show the globe rotation and the zoom-out/zoom-in arc clearly.
    computeFlightDuration(lat, lng, targetZoom) {
      if (!this.map) {
        return 1500;
      }
      const center = this.map.getCenter();
      const toRad = degrees => (degrees * Math.PI) / 180;
      const dLat = toRad(lat - center.lat);
      const dLng = toRad(lng - center.lng);
      const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRad(center.lat)) * Math.cos(toRad(lat)) * Math.sin(dLng / 2) ** 2;
      const distanceKm = 2 * 6371 * Math.asin(Math.min(1, Math.sqrt(a)));
      const distanceFactor = Math.min(distanceKm / 20015, 1);
      const zoomDelta = Math.abs(targetZoom - this.map.getZoom());
      const duration = 1500 + distanceFactor * 4000 + zoomDelta * 80;
      return Math.max(1500, Math.min(duration, 6500));
    },
    // Two-stage flight for cross-country transitions: zoom out to the globe,
    // hold there so the journey is noticeable, then travel into the target.
    flyToWithTravelPause(coordinates, zoomLevel, onComplete) {
      if (!this.map) {
        return;
      }

      let lat = coordinates && coordinates.length ? parseFloat(coordinates[0]) : NaN;
      let lng = coordinates && coordinates.length ? parseFloat(coordinates[1]) : NaN;
      if (isNaN(lat) || isNaN(lng)) {
        lng = defaultCenter[0];
        lat = defaultCenter[1];
      }
      const targetZoom = zoomLevel || 4;
      const origin = this.map.getCenter();
      const pauseZoom = this.globeFitZoom != null ? this.globeFitZoom : 2;

      // Cancel any in-progress travel pause
      if (this.travelPauseTimeout) {
        clearTimeout(this.travelPauseTimeout);
        this.travelPauseTimeout = null;
      }
      if (this.travelMoveHandler) {
        this.map.off('moveend', this.travelMoveHandler);
        this.travelMoveHandler = null;
      }

      this.map.resize();

      // Stage 1: zoom out over the origin to reveal the globe
      this.map.flyTo({ center: [origin.lng, origin.lat], zoom: pauseZoom, duration: 1600 });

      this.travelMoveHandler = () => {
        if (!this.map) {
          return;
        }
        this.map.off('moveend', this.travelMoveHandler);
        this.travelMoveHandler = null;

        // Hold at the zoomed-out view so the travel is perceptible
        this.travelPauseTimeout = setTimeout(() => {
          this.travelPauseTimeout = null;
          if (!this.map) {
            return;
          }
          // Stage 2: travel across the globe into the target
          this.map.flyTo({
            center: [lng, lat],
            zoom: targetZoom,
            duration: this.computeFlightDuration(lat, lng, targetZoom),
          });
          if (onComplete && typeof onComplete === 'function') {
            this.map.once('moveend', onComplete);
          }
        }, this.travelPauseMs);
      };
      this.map.once('moveend', this.travelMoveHandler);
    },
    openPopup(latitude, longitude, content) {
      if (!this.map) {
        return;
      }
      const lat = parseFloat(latitude);
      const lng = parseFloat(longitude);
      if (isNaN(lat) || isNaN(lng)) {
        return;
      }
      if (this.popup) {
        this.popup.remove();
      }
      this.popup = new maplibregl.Popup({ offset: [0, -48], maxWidth: '360px' })
        .setLngLat([lng, lat])
        .setHTML(content)
        .addTo(this.map);
    },
    // Public method to fit viewport when map becomes visible (e.g., on mobile)
    fitViewportWhenVisible() {
      // Ensure the map is initialised now that the panel is actually visible.
      // On some mobile browsers the deferred ResizeObserver init never fires, so
      // trigger it explicitly here (loadMap is idempotent).
      this.loadMap();

      if (!this.map) {
        return;
      }
      // Wait for the map container to be fully visible in the DOM
      const reveal = (attempt = 0) => {
        if (!this.map) {
          // Map may still be initialising after the panel became visible
          if (attempt < 20) {
            setTimeout(() => reveal(attempt + 1), 50);
          }
          return;
        }
        // Resize first - critical when the container was previously hidden (display: none)
        this.map.resize();

        // Match a fresh desktop load: globe fitted to the container, centred on the Philippines
        const targetZoom = this.globeFitZoom ?? this.map.getZoom();
        this.mapZoom = targetZoom;
        this.map.jumpTo({ center: defaultCenter, zoom: targetZoom });
      };
      setTimeout(() => reveal(), 100);
    },
    fitMapToMarkers() {
      if (!this.map) {
        return;
      }

      const points = (this.merchants || [])
        .map(merchant => [parseFloat(merchant.longitude), parseFloat(merchant.latitude)])
        .filter(coord => !isNaN(coord[0]) && !isNaN(coord[1]));

      if (points.length === 0) {
        return;
      }

      const bounds = points.reduce(
        (acc, coord) => acc.extend(coord),
        new maplibregl.LngLatBounds(points[0], points[0])
      );

      this.map.fitBounds(bounds, {
        padding: 20,
        maxZoom: 12,
        duration: 1500,
      });
    },
    // Close any open merchant popup card
    closePopup() {
      if (this.popup) {
        this.popup.remove();
        this.popup = null;
      }
    },
    // Fly the globe back to its optimal (fit) zoom level
    returnToGlobeFit() {
      if (!this.map) {
        return;
      }

      const targetZoom = this.globeFitZoom ?? this.map.getZoom();
      this.mapZoom = targetZoom;

      this.map.flyTo({
        center: defaultCenter,
        zoom: targetZoom,
        duration: 1800,
      });
    },
  },
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  min-height: 0;
  background: radial-gradient(
    circle at 50% 50%,
    rgb(var(--map-glow-1)) 0%,
    rgb(var(--map-glow-2)) 45%,
    rgb(var(--map-glow-3)) 78%
  );
}

.map-container :deep(.maplibregl-map) {
  height: 100% !important;
  width: 100% !important;
}

.map-error {
  position: absolute;
  inset: 0;
  z-index: 6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem;
  text-align: center;
}

.map-error__title {
  font-family: 'Baloo 2', ui-rounded, system-ui, sans-serif;
  font-size: 1.125rem;
  font-weight: 700;
  color: rgb(var(--ink));
}

.map-error__text {
  max-width: 24rem;
  font-size: 0.875rem;
  color: rgb(var(--ink-muted));
}

.globe-home-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 5;
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 9999px;
  border: 1px solid rgb(var(--soft));
  background-color: rgb(var(--card));
  color: rgb(var(--ink));
  box-shadow: 0 10px 24px -10px rgba(15, 23, 42, 0.35);
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

.globe-home-btn:hover {
  background-color: rgb(var(--brand-600));
  color: #fff;
  transform: translateY(-1px);
}

.globe-home-btn:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgb(var(--cloud)), 0 0 0 5px rgb(var(--brand-500));
}
</style>

<style>
/* Merchant popup card */
.maplibregl-popup-content {
  padding: 18px 20px;
  border-radius: 16px;
  border: 1px solid rgb(var(--soft));
  background-color: rgb(var(--card));
  box-shadow: var(--popup-shadow);
  font-family: inherit;
  animation: popup-ease-up 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  transform-origin: bottom center;
}

.maplibregl-popup-close-button {
  top: 6px;
  right: 6px;
  width: 26px;
  height: 26px;
  border-radius: 9999px;
  font-size: 18px;
  line-height: 1;
  color: rgb(var(--ink-faint));
  transition: background-color 0.15s ease, color 0.15s ease;
}

.maplibregl-popup-close-button:hover {
  background-color: rgb(var(--brand-50));
  color: rgb(var(--ink));
}

/* Popup ease-in animation from below */
@keyframes popup-ease-up {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
