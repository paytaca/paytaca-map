<template>
    <div class="p-4">
      <div v-for="logo in logos" :key="logo.id" class="flex items-center mb-4">
        <img :src="logo.url" :alt="logo.location.name" class="w-12 h-12 mr-2 rounded-full">
        <p>{{ logo.location.name }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'LogoList',
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
        axios.get('http://localhost:8000/logos/') // Change URL as per your Django server address
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
  
  <style scoped>
  /* Add any necessary styles for logos here */
  </style>
  