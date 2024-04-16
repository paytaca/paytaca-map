<template>
    <div class="p-4 overflow-y-auto h-full">
      <div class="grid grid-cols-3 gap-4"> <!-- Use grid layout with 3 columns -->
        <div v-for="logo in logos" :key="logo.id" class="m-2">
          <img :src="logo.url" :alt="logo.location.name" class="w-24 h-24 object-cover" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'LocationLogos',
    data() {
      return {
        logos: [],
      };
    },
    mounted() {
      this.fetchLogos();
    },
    methods: {
      fetchLogos() {
        axios.get('http://localhost:8000/logos/') // Adjust URL as per your backend API endpoint
          .then(response => {
            this.logos = response.data;
          })
          .catch(error => {
            console.error('Error fetching logos:', error);
          });
      }
    }
  };
  </script>
  