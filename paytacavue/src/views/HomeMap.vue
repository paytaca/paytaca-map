<template>
  <div class="w-full h-screen">
    <MapView />
  </div>
</template>

<script>
import MapView from '@/components/MapView.vue';

export default {
  name: 'HomeMap',
  components: {
    MapView,
  },
};
</script>
